#!/bin/dash
# Autostart script for kiosk mode, based on @AYapejian: https://github.com/MichaIng/DietPi/issues/1737#issue-318697621

# Resolution to use for kiosk mode, should ideally match current system resolution
RES_X=$(sed -n '/^[[:blank:]]*SOFTWARE_CHROMIUM_RES_X=/{s/^[^=]*=//p;q}' /boot/dietpi.txt)
RES_Y=$(sed -n '/^[[:blank:]]*SOFTWARE_CHROMIUM_RES_Y=/{s/^[^=]*=//p;q}' /boot/dietpi.txt)

# Command line switches: https://peter.sh/experiments/chromium-command-line-switches/
# - Review and add custom flags in: /etc/chromium.d
CHROMIUM_OPTS="--kiosk --window-size=${RES_X:-1280},${RES_Y:-720} --window-position=0,0"

CHROMIUM_OPTS="--kiosk --no-crash-upload --disable-breakpad --disable-crash-reporter --incognito --disable-translate --no-first-run --fast --fast-start --disable-features=TranslateUI --disk-cache-dir=/dev/null --disk-cache-size=1 --password-store=basic --noerrdialogs --window-size=${RES_X:-1920},${RES_Y:-1080} --window-position=0,0"
# If you want tablet mode, uncomment the next line.
#CHROMIUM_OPTS+=' --force-tablet-mode --tablet-ui'

# Home page
URL=$(sed -n '/^[[:blank:]]*SOFTWARE_CHROMIUM_AUTOSTART_URL=/{s/^[^=]*=//p;q}' /boot/dietpi.txt)

# RPi or Debian Chromium package
FP_CHROMIUM=$(command -v chromium-browser)
[ "$FP_CHROMIUM" ] || FP_CHROMIUM=$(command -v chromium)

# Use "startx" as non-root user to get required permissions via systemd-logind
STARTX='xinit'
[ "$USER" = 'root' ] || STARTX='startx'

check_url() {
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8123/huffbox-dashboard | grep -q "200"; then
        return 0
    else
        return 1
    fi
}

# Loop until we get a 200 status code
while ! check_url; do
    sleep 5
done

exec "$STARTX" "$FP_CHROMIUM" $CHROMIUM_OPTS "${URL:-https://dietpi.com/}"
