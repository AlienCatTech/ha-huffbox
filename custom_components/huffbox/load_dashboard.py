import logging

from homeassistant.components import frontend
from homeassistant.components.lovelace.dashboard import LovelaceYAML
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def load_dashboard(hass: HomeAssistant, config_entry) -> None:
    sidepanel_title = DOMAIN + " Dashboard"
    sidepanel_icon = "mdi:alpha-d-box"

    dashboard_url = "huffbox-dashboard"
    dashboard_config = {
        "mode": "yaml",
        "icon": sidepanel_icon,
        "title": sidepanel_title,
        "filename": "custom_components/huffbox/huffui/ui-lovelace.yaml",
        "show_in_sidebar": True,
        "require_admin": False,
    }

    config = LovelaceYAML(hass, dashboard_url, dashboard_config)

    # hass.data["lovelace"]["dashboards"][dashboard_url] = LovelaceYAML(
    #     hass, dashboard_url, dashboard_config)

    # _register_panel(hass, dashboard_url, "yaml", dashboard_config, False)

    hass.http.register_static_path(
        "/huffbox/huffui",
        hass.config.path("custom_components/huffbox/huffui"),
        cache_headers=False,
    )
    frontend.add_extra_js_url(hass, "/huffbox/huffui/huffui.js")

    # frontend.async_register_built_in_panel(hass, DOMAIN, "HuffBox", 'mdi:view-dashboard-variant', dashboard_url, config={
    #     "_panel_custom": {
    #         "name": "custom-sidebar-panel",
    #         "module_url": "/huffbox/huffui/custom-sidebar-panel.js",
    #         "embed_iframe": True,
    #     }
    # })
    frontend.async_register_built_in_panel(
        hass,
        "huffbox-ui",
        "HuffBox",
        "mdi:view-dashboard-variant",
        "huffbox-dashboard",
        config.config,
    )
