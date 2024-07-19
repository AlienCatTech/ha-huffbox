FROM homeassistant/home-assistant:latest

RUN apk add --no-cache libgpiod
RUN pip install gpiod==2.2.0 luma.led-matrix==1.7.1
COPY ./custom_components/huffbox /setup/custom_components/huffbox
RUN addgroup -S -g 1000 user && adduser -S -u 1000 -G user user && \
    addgroup -S -g 994 gpio && adduser user gpio && \
    addgroup -S -g 996 spi && adduser user spi && \
    addgroup -S -g 29 audio1 && adduser user audio1
COPY entrypoint.sh /entrypoint.sh
RUN mkdir -p /config && chown -R 1000:1000 /config
USER 1000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python3", "-m", "homeassistant", "--config", "/config"]
