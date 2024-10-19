import ssl
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import netifaces
from homeassistant.core import HomeAssistant


def get_current_dir() -> Path:
    return Path(__file__).parent.resolve()


def get_config_dir(hass: HomeAssistant) -> Path:
    return Path(hass.config.config_dir)


def countdown_until(time_string: str) -> str:
    # Parse the input time string
    hours, minutes, seconds = map(int, time_string.split(":"))

    # Create a datetime object for the target time
    now = datetime.now()  # noqa: DTZ005
    target_time = now.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)

    # If the target time is earlier than now, set it to tomorrow
    if target_time < now:
        target_time += timedelta(days=1)

    # Calculate the difference in seconds
    diff_seconds = int((target_time - now).total_seconds())

    # Convert seconds to hh:mm:ss format
    countdown_hours = diff_seconds // 3600
    countdown_minutes = (diff_seconds % 3600) // 60
    countdown_seconds = diff_seconds % 60

    # Pad with zeros and return the formatted string
    return f"{countdown_hours:02d}:{countdown_minutes:02d}:{countdown_seconds:02d}"


def snake_to_title(snake_str: str) -> str:
    return " ".join(word.capitalize() for word in snake_str.split("_"))


def get_all_lan_ips() -> str:
    lan_ips = []
    interfaces = netifaces.interfaces()

    for interface in interfaces:
        try:
            addr = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
            if addr:
                for link in addr:
                    ip = link["addr"]
                    if ip != "127.0.0.1":
                        lan_ips.append((interface, ip))
        except ValueError:
            pass

    return ",".join(lan_ips)


def get_state(hass: HomeAssistant, state: str, default: Any) -> Any:
    s = hass.states.get(state)
    if s:
        return s.state
    return default


GPIO_VALUES = {"ambient_gpio": 13, "fan_gpio": 19, "lock_gpio": 26, "pixel_gpio": 6}

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def www_to_link(hass: HomeAssistant, path: Path) -> str:
    prefix = str(get_config_dir(hass) / "www")
    s = str(path)
    return s.replace(prefix, "/local")
