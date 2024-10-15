import json
from datetime import timedelta
from pathlib import Path
from typing import Any

import homeassistant.util.dt as dt_util
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import template
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_point_in_time
from jsonschema import validate as json_validate

from custom_components.huffbox.common import get_current_dir

from .const import DOMAIN, LOGGER
from .entity import HuffBoxBaseEntity

SCHEMAS = Path("./scene_studio.schema.json")


class SceneStudio(HuffBoxBaseEntity, Entity):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize SceneStudio."""
        super().__init__(config_entry, "scene_studio")
        self.hass = hass
        self.entity_id = DOMAIN + ".scene_studio"
        self._state = "idle"
        self._timers = {}
        with Path.open(get_current_dir() / SCHEMAS) as schema_file:
            self.schema = json.load(schema_file)

    def validate(self, data: Any) -> bool:
        try:
            # Validate the incoming JSON against the schema
            json_validate(instance=data, schema=self.schema)
            return True  # noqa: TRY300
        except Exception as e:
            LOGGER.error("Failed to validate Scene Preset", e)
            return False

    def _set_state(self, state: str) -> None:
        self._state = state
        async_dispatcher_send(self.hass, "update_huffbox_scene_studio_current", state)

    def _parse_time_string(self, time_str: str) -> timedelta | None:
        try:
            parts = time_str.split(":")

            hours, minutes, seconds = map(int, parts)

            return timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            return None

    def _async_call_service(self, service: dict, time_str: str) -> Any:
        async def call_service(*_: Any) -> None:
            domain, service_name = service.get("service", "").split(".")
            data = service.get("data", {})
            target = service.get("target")
            self._set_state(f"[{time_str}] - {service}")
            t = template.Template(json.dumps(data), self.hass)

            await self.hass.services.async_call(
                domain, service_name, t.async_render(), target=target
            )
            # Remove the timer using the known time_str
            self._timers.pop(time_str, None)
            self._check_and_update_state()

        return call_service

    def _check_and_update_state(self) -> None:
        if not self._timers:
            self._set_state("idle")
            self.async_schedule_update_ha_state()

    async def start(self, data: Any) -> None:
        if self._state == "idle":
            file = await self.huffbox.media_manager.get_file(data)

            schedules = json.loads(file)
            for timer in self._timers.values():
                timer()
            self._timers.clear()
            if self.validate(schedules):
                now = dt_util.utcnow()
                for time_str, service_list in schedules.items():
                    delay = self._parse_time_string(time_str)
                    if delay is None:
                        continue

                    run_at = now + delay
                    for service in service_list:
                        self._timers[time_str] = async_track_point_in_time(
                            self.hass,
                            self._async_call_service(service, time_str),
                            run_at,
                        )
                self._set_state(f"Scene Started with {len(self._timers)} services")
                self.async_schedule_update_ha_state()

    def stop(self) -> None:
        """Stop all scheduled services and reset the state."""
        for timer in self._timers.values():
            timer()
        self._timers.clear()
        self._set_state("idle")
        self.async_schedule_update_ha_state()
