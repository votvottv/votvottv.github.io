#
# Dockerfile for Landing Pages development.
#

FROM python:3.8-bullseye
MAINTAINER Silvio Rhatto <rhatto@torproject.org>

ENV APP="${COMPOSE_PROJECT_NAME:-sponsor123-landing-page}"
ENV APP_BASE="/srv"
ENV SHELL="/bin/bash"

# UID and GID might be read-only values, so use non-conflicting ones
ARG CONTAINER_UID="${CONTAINER_UID:-1000}"
ARG CONTAINER_GID="${CONTAINER_GID:-1000}"

WORKDIR ${APP_BASE}/${APP}

# Slower approach, root user
COPY . ${APP_BASE}/${APP}
RUN  ${APP_BASE}/${APP}/scripts/provision
RUN  rm -rf /var/lib/apt/lists/*

# Switch to a regular user
RUN groupadd -r -g ${CONTAINER_GID} ${APP} && \
    useradd --no-log-init -r -u ${CONTAINER_UID} -g ${APP} ${APP} && \
    mkdir -p /home/${APP} && chown ${APP}. /home/${APP}
RUN chown -R ${APP}.${APP} ${APP_BASE}/${APP}
USER ${APP}

# Initial build
#RUN ${APP_BASE}/${APP}/scripts/build

ENTRYPOINT [ "scripts/server" ]
