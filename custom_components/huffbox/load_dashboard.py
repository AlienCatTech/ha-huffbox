from homeassistant.components import frontend
from homeassistant.components.lovelace.dashboard import LovelaceYAML
from homeassistant.core import HomeAssistant

from .const import DOMAIN


def load_dashboard(hass: HomeAssistant) -> None:
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

    hass.http.register_static_path(
        "/huffbox/huffui",
        hass.config.path("custom_components/huffbox/huffui"),
        cache_headers=False,
    )
    frontend.add_extra_js_url(hass, "/huffbox/huffui/huffui.js")
    frontend.async_register_built_in_panel(
        hass,
        "huffbox-ui",
        "HuffBox",
        "mdi:view-dashboard-variant",
        "huffbox-dashboard",
        config.config,
    )
