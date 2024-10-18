import socket
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

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


def get_lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(("10.0.0.0", 0))
        ip = s.getsockname()[0]
    except Exception:
        ip = socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
    return ip


def get_state(hass: HomeAssistant, state: str, default: Any) -> Any:
    s = hass.states.get(state)
    if s:
        return s.state
    return default


GPIO_VALUES = {"ambient_gpio": 13, "fan_gpio": 19, "lock_gpio": 26, "pixel_gpio": 6}
