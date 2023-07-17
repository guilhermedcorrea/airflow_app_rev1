

FROM debian:10

WORKDIR /root

SHELL ["/bin/bash", "-o", "pipefail", "-c"]


RUN echo APT::Install-Recommends "0"\; > /etc/apt/apt.conf.d/10disableextras
RUN echo APT::Install-Suggests "0"\; >>  /etc/apt/apt.conf.d/10disableextras

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_TERSE true


COPY pkg-resolver pkg-resolver
RUN chmod a+x pkg-resolver/install-pkg-resolver.sh
RUN pkg-resolver/install-pkg-resolver.sh debian:10

RUN apt-get -q update \
    && apt-get -q install -y --no-install-recommends $(pkg-resolver/resolve.py debian:10) \
    && echo 'deb http://deb.debian.org/debian bullseye main' >> /etc/apt/sources.list \
    && apt-get -q update \
    && apt-get -q install -y --no-install-recommends -t bullseye $(pkg-resolver/resolve.py --release=bullseye debian:10) \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


ENV MAVEN_HOME /usr

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64


ENV SPOTBUGS_HOME /opt/spotbugs


ENV PROTOBUF_HOME /opt/protobuf
ENV PATH "${PATH}:/opt/protobuf/bin"


ENV MAVEN_OPTS -Xms256m -Xmx3072m


ENV HADOOP_SKIP_YETUS_VERIFICATION true


RUN pkg-resolver/install-cmake.sh debian:10
RUN pkg-resolver/install-spotbugs.sh debian:10
RUN pkg-resolver/install-boost.sh debian:10
RUN pkg-resolver/install-protobuf.sh debian:10
RUN pkg-resolver/install-hadolint.sh debian:10
RUN pkg-resolver/install-intel-isa-l.sh debian:10


COPY hadoop_env_checks.sh /root/hadoop_env_checks.sh
RUN chmod 755 /root/hadoop_env_checks.sh

RUN echo '${HOME}/hadoop_env_checks.sh' >> /root/.bashrc