from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components import frontend
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from custom_components.huffbox.scene_studio import SceneStudio
from custom_components.huffbox.view import HuffBoxDownloadView, HuffBoxUploadView

from .const import DOMAIN, LOGGER
from .data import HuffBoxConfigEntry, HuffBoxData
from .huffbox import HuffBox
from .load_dashboard import load_dashboard
from .random_coordinator import RandomNumberCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall


PLATFORMS: list[str] = [
    Platform.SENSOR,
    Platform.LIGHT,
    Platform.TEXT,
    Platform.FAN,
    Platform.LOCK,
    Platform.SELECT,
    Platform.TIME,
    Platform.BUTTON,
    Platform.NUMBER,
]


async def async_setup_entry(hass: HomeAssistant, entry: HuffBoxConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    huffbox = HuffBox(hass, entry)
    await huffbox.gpio.start()
    random_coordinator = RandomNumberCoordinator(hass, huffbox)
    await random_coordinator.async_config_entry_first_refresh()
    entry.runtime_data = HuffBoxData(
        huffbox=huffbox,
        random_coordinator=random_coordinator,
    )
    entry.async_on_unload(huffbox.close)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    await load_dashboard(hass)

    scene_studio = SceneStudio(hass, entry)
    huffbox.scene_studio = scene_studio

    upload_view = HuffBoxUploadView(hass, huffbox.media_manager)
    download_view = HuffBoxDownloadView(hass, huffbox.media_manager)
    hass.http.register_view(upload_view)
    hass.http.register_view(download_view)

    async def toggle_lock_service(call: ServiceCall) -> None:
        entity_id = call.data.get("entity_id")
        if not entity_id:
            return
        lock = hass.states.get(entity_id)
        if lock is None:
            LOGGER.error(f"Entity {entity_id} not found")
            return
        if lock.state == "locked":
            await hass.services.async_call("lock", "unlock", {"entity_id": entity_id})
        else:
            await hass.services.async_call("lock", "lock", {"entity_id": entity_id})

    hass.services.async_register("lock", "toggle", toggle_lock_service)

    LOGGER.info("HuffBox Loaded")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: HuffBoxConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    frontend.async_remove_panel(hass, "huffbox-dashboard")
    if unload_ok and DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: HuffBoxConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
