import json
from datetime import timedelta
from pathlib import Path
from typing import Any
from uu import Error

import homeassistant.util.dt as dt_util
from homeassistant.components.media_player import (
    MediaPlayerEntity,
)
from homeassistant.components.media_player.const import (
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import template
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from jsonschema import validate as json_validate

from custom_components.huffbox.common import get_current_dir
from custom_components.huffbox.const import LOGGER

from .data import HuffBoxConfigEntry
from .entity import HuffBoxBaseEntity

SCHEMAS = Path("./scene_studio.schema.json")


def get_last_key_as_seconds(time_dict: dict) -> int | None:
    if not time_dict:
        return None

    last_key = list(time_dict.keys())[-1]

    time_delta = parse_time_string(last_key)
    if time_delta is None:
        return None

    return int(time_delta.total_seconds())


def parse_time_string(time_str: str) -> timedelta | None:
    try:
        parts = time_str.split(":")

        hours, minutes, seconds = map(int, parts)

        return timedelta(hours=hours, minutes=minutes, seconds=seconds)
    except ValueError:
        return None


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001
    entry: HuffBoxConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities([HuffBoxSceneStudioPlayer(entry)], update_before_add=True)


class HuffBoxSceneStudioPlayer(HuffBoxBaseEntity, CoordinatorEntity, MediaPlayerEntity):
    _attr_supported_features = (
        MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.STOP
        | MediaPlayerEntityFeature.SELECT_SOURCE
    )

    def __init__(self, config_entry: HuffBoxConfigEntry) -> None:
        super().__init__(config_entry, "scene_studio")
        CoordinatorEntity.__init__(self, config_entry.runtime_data.random_coordinator)
        self.state = MediaPlayerState.ON
        self._timers = {}
        self._position = 0

    @property
    def media_position(self) -> int:
        return self.coordinator.data["media_player_second_passed"](
            self.update_second_passed
        )

    def update_second_passed(self) -> int | None:
        if self.state == MediaPlayerState.PLAYING:
            if self._position:
                self._position += 1
            else:
                self._position = 1
        else:
            self._position = None

        self.media_position_updated_at = dt_util.utcnow()

        return self._position

    def _validate(self, data: Any) -> bool:
        try:
            # Validate the incoming JSON against the schema
            json_validate(instance=data, schema=self.schema)
            return True  # noqa: TRY300
        except Exception as e:
            LOGGER.error("Failed to validate Scene Preset", e)
            return False

    def _async_call_service(self, service: dict, time_str: str) -> Any:
        async def call_service(*_: Any) -> None:
            domain, service_name = service.get("service", "").split(".")
            data = service.get("data", {})
            target = service.get("target", {})
            self.media_title = f"{service_name}: {target['entity_id']}"
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
            self.state = MediaPlayerState.IDLE
            self.async_schedule_update_ha_state()

    async def load_scene_studio_options(self) -> list[str]:
        scene_studio_presets = await self.huffbox.media_manager.list_files()

        return [x.name for x in scene_studio_presets]

    async def start(self, data: str) -> None:
        file = await self.huffbox.media_manager.get_file(data)

        schedules = json.loads(file)

        for timer in self._timers.values():
            timer()
        self._timers.clear()
        if self._validate(schedules):
            self.state = MediaPlayerState.PLAYING
            self.media_duration = get_last_key_as_seconds(schedules)
            self.media_playlist = self.source

            now = dt_util.utcnow()
            for time_str, service_list in schedules.items():
                delay = parse_time_string(time_str)
                if delay is None:
                    continue

                run_at = now + delay
                for service in service_list:
                    self._timers[time_str] = async_track_point_in_time(
                        self.hass,
                        self._async_call_service(service, time_str),
                        run_at,
                    )
            self.async_schedule_update_ha_state()
        else:
            msg = "file invalid"
            raise Error(msg)

    def stop(self) -> None:
        """Stop all scheduled services and reset the state."""
        for timer in self._timers.values():
            timer()
        self.state = MediaPlayerState.IDLE
        self.media_playlist = None
        self.async_schedule_update_ha_state()

    async def async_media_play(self) -> None:
        if not self.source:
            msg = "No source selected"
            raise Error(msg)
        await self.start(self.source)

    async def async_media_stop(self) -> None:
        self.stop()

    def async_select_source(self, source: str) -> None:
        self.source = source

    @property
    def media_content_type(self) -> MediaType:
        return MediaType.PLAYLIST

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        self.source_list = await self.load_scene_studio_options()
        with Path.open(get_current_dir() / SCHEMAS) as schema_file:
            self.schema = json.load(schema_file)

    async def async_update(self) -> None:
        self.source_list = await self.load_scene_studio_options()
