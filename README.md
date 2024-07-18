# HuffBox

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]

_Integration to integrate with [huffbox][huffbox]._

## Prerequisite
**You need to have libgpiod installed on your homeassistant system (container or host etc)**

Debian, Ubuntu
```bash
sudo apt install -y libgpiod-dev
```
Alpine
```bash
sudo apk add libgpiod
```

You also need to enable GPIO and SPI on your Raspi.

## Installation
This custom integration uses low level hardware IO (SPI and GPIO), so it's a little different than other integrations.

### Using Patched Docker Image
This patched home assistant image is all you need `ghcr.io/AlienCatTech/ha-huffbox:latest`
> The only patch applied is adding libgpiod to the latest official home assistant image

### Manual Install
1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `huffbox`.
1. Download zip from [Releases](https://github.com/AlienCatTech/ha-huffbox/releases)
1. Unzip and place the files you downloaded in the custom_components. So like `custom_components/huffbox`
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "HuffBox"

## Docker Compose
Please use the docker-compose.yaml file in the repo to setup your docker container. As RAW IO access is required.

## Config
### Kiosk mode
HuffBox dashboard is designed running in a chromium kiosk mode without any manual input. You can use `http://localhost:8123/huffbox-dashboard?kiosk`. The kiosk query param is to hide the side bar.

## Entities

**This integration will set up the following platforms.**

Platform | Description
-- | --
`button.refresh_button` | refresh all browsers that loads HuffBox dashboard
`fan.control_fan` | build-in fan
`light.control_light` | build-in light
`light.led` | build-in matrix LED display. you can pass attr for changing light mode.
`lock.control_lock` | build-in electric magnetic lock
`number.gpio_pin_light` | GPIO pin number for light relay
`number.gpio_pin_fan` | GPIO pin number for fan relay
`number.gpio_pin_lock` | GPIO pin number for lock relay
`select.select_dashboard` | select dashboard layout
`sensor.heart_rate` | mock heart rate
`sensor.pulse` | mock pulse
`sensor.spo2` | mock spo2
`sensor.resp` | mock resp
`sensor.temp` | mock temp
`sensor.second_passed` | counting how many seconds door is locked
`sensor.lan_ip` | LAN IP address for wifi access
`text.subject_name` | name displayed in the dashboard
`text.subject_picture` | picture url displayed in the dashboard. you can also upload directly from dashboard
`text.custom_layout_link` | layout json url for the dashboard. this is used when you select custom in `select.select_dashboard`
`text.custom_led_text` | text displayed in the LED matrix. this is used when you select custom in `light.led`
`text.banner` | text displayed in banner section of the dashboard
`text.live_chat` | text displayed in live_chat section of the dashboard
`text.video_link` | picture url displayed in the dashboard. this is used when you use video player component in the dashboard
`time.time` | for counting down until the lock opens

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[huffbox]: https://github.com/aliencattech/huffbox
[commits-shield]: https://img.shields.io/github/commit-activity/y/aliencattech/huffbox.svg?style=for-the-badge
[commits]: https://github.com/aliencattech/huffbox/commits/main
[exampleimg]: example.png
[releases-shield]: https://img.shields.io/github/release/aliencattech/huffbox.svg?style=for-the-badge
[releases]: https://github.com/aliencattech/huffbox/releases
