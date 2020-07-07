FROM alpine

RUN apk --no-cache --no-progress upgrade && \
    apk --no-cache --no-progress add bash curl privoxy shadow tini tor tzdata&&\
    mkdir -p /etc/tor/run && \
    chown -Rh tor. /var/lib/tor /etc/tor/run && \
    chmod 0750 /etc/tor/run && \
    rm -rf /tmp/*

COPY docker/torproxy.sh /usr/bin/

EXPOSE 8118 9050 9051

HEALTHCHECK --interval=60s --timeout=15s --start-period=20s \
            CMD curl -sx localhost:8118 'https://check.torproject.org/' | \
            grep -qm1 Congratulations

VOLUME ["/etc/tor","/etc/privoxy", "/var/lib/tor"]

ENTRYPOINT ["/sbin/tini", "--", "/usr/bin/torproxy.sh"]
