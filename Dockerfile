FROM ubuntu:20.04

WORKDIR /usr/src/app
SHELL ["/bin/bash", "-c"]
RUN chmod 777 /usr/src/app
     
RUN apt-get -qq update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -qq install -y tzdata aria2 git python3 python3-pip \
    libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 \ 
    libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 \ 
    libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \ 
    libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \ 
    libnss3 libgbm-dev \
    locales python3-lxml \
    curl pv jq ffmpeg \
    p7zip-full p7zip-rar \
    libcrypto++-dev libssl-dev \
    libc-ares-dev libcurl4-openssl-dev \
    libsqlite3-dev libsodium-dev && \
    curl -L https://github.com/lzzy12/megasdkrest/releases/download/v0.1.14-rebuild/megasdkrest-$(cpu=$(uname -m); if [[ "$cpu" == "x86_64" ]]; then    echo "amd64"; elif [[ "$cpu" == "x86" ]]; then    echo "i386"; elif [[ "$cpu" == "aarch64" ]]; then    echo "arm64"; else    echo $cpu; fi) -o /usr/local/bin/megasdkrest && \
    chmod +x /usr/local/bin/megasdkrest \
    curl -L https://github.com/FlareSolverr/FlareSolverr/releases/download/v1.2.5/flaresolverr-v1.2.5-linux-x64.zip -o /usr/local/bin/flaresolverr.zip && \
    7z x /usr/local/bin/flaresolverr.zip -o/usr/local/bin && \
    mv /usr/local/bin/flaresolverr /usr/local/bin/flaresolverr1 && \
    mv /usr/local/bin/flaresolverr1/flaresolverr /usr/local/bin/flaresolverr && \
    mv /usr/local/bin/flaresolverr1/chrome /usr/local/bin/chrome && \
    chmod +x /usr/local/bin/flaresolverr

COPY requirements.txt .
COPY extract /usr/local/bin
RUN chmod +x /usr/local/bin/extract
RUN pip3 install --no-cache-dir -r requirements.txt && \
    apt-get -qq purge git

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
COPY . .
COPY netrc /root/.netrc
RUN chmod +x aria.sh
RUN chmod +x flaresolverr.sh

CMD ["bash","start.sh"]
