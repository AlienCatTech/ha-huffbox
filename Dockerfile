FROM homeassistant/home-assistant:2024.10.3

RUN apk add --no-cache libgpiod rsync
COPY ./custom_components/huffbox /setup/custom_components/huffbox
COPY entrypoint.sh /entrypoint.sh
COPY requirements.txt /tmp/requirements.txt
RUN addgroup -S -g 1000 user && adduser -S -u 1000 -G user user && \
    addgroup -S -g 994 gpio && adduser user gpio && \
    addgroup -S -g 996 spi && adduser user spi && \
    addgroup -S -g 29 audio1 && adduser user audio1
RUN  mkdir -p /config && chown -R 1000:1000 /config && chown 1000:1000 /tmp/requirements.txt
USER 1000
RUN pip install -r /tmp/requirements.txt
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python3", "-m", "homeassistant", "--config", "/config"]
