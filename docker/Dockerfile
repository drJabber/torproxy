FROM python:3.8-slim-buster

ENV TINI_VERSION v0.18.0

RUN apt-get update -y && \
    apt-get install --no-install-recommends --no-install-suggests -y \ 
        apt-transport-https \
        ca-certificates \
        dirmngr \
        apt-utils \
        gnupg \
        curl \    
        procps privoxy tzdata && \
    # Add torproject.org Debian repository for stable Tor version \
    curl https://deb.torproject.org/torproject.org/A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89.asc | gpg --import && \
    gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add - && \
    echo "deb https://deb.torproject.org/torproject.org buster main"   >  /etc/apt/sources.list.d/tor-apt-sources.list && \
    echo "deb-src https://deb.torproject.org/torproject.org buster main" >> /etc/apt/sources.list.d/tor-apt-sources.list && \
    #install tini
    curl -L https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini -o /sbin/tini && \
    chmod +x /sbin/tini && \
    # Install tor \
    apt-get update -y && \
    apt-get install --no-install-recommends --no-install-suggests -y \ 
        tor \
        deb.torproject.org-keyring && \
    mkdir -pv /usr/local/etc/tor/ && \
    mv -v /etc/tor/torrc /usr/local/etc/tor/torrc.sample && \
    apt-get purge --auto-remove -y \
            apt-transport-https \
            dirmngr \
            apt-utils \
            gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Rename Debian unprivileged user to tord \
    usermod -l tord debian-tor && \
    groupmod -n tord debian-tor && \
    mkdir /app && \
    rm -rf /tmp/* 

ADD docker/entrypoint.sh /usr/bin/
ADD ./switcher/* /app/
EXPOSE 8951 9050 8118

HEALTHCHECK --interval=60s --timeout=15s --start-period=20s \
            CMD curl -sx localhost:8118 'https://check.torproject.org/' | \
            grep -qm1 Congratulations

VOLUME ["/etc/tor","/etc/privoxy"]

ENTRYPOINT ["/sbin/tini", "--","/usr/bin/entrypoint.sh"] 
# ENTRYPOINT ["/usr/bin/entrypoint.sh"] 