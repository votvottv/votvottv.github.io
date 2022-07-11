#
# Dockerfile for Landing Pages development.
#

FROM python:3.8-bullseye AS landing
MAINTAINER Silvio Rhatto <rhatto@torproject.org>

# Basic project environment
ENV APP="${COMPOSE_PROJECT_NAME:-onion-launchpad}"
ENV APP_BASE="/srv"
ENV SHELL="/bin/bash"

# UID and GID might be read-only values, so use non-conflicting ones
ARG CONTAINER_UID="${CONTAINER_UID:-1000}"
ARG CONTAINER_GID="${CONTAINER_GID:-1000}"

WORKDIR ${APP_BASE}/${APP}

# Copy the project files and run the provision script
COPY . ${APP_BASE}/${APP}
RUN  ${APP_BASE}/${APP}/scripts/provision
RUN  rm -rf /var/lib/apt/lists/*

# Switch to a regular user
RUN groupadd -r -g ${CONTAINER_GID} ${APP} && \
    useradd --no-log-init -r -u ${CONTAINER_UID} -g ${APP} ${APP} && \
    mkdir -p /home/${APP} && chown ${APP}. /home/${APP}
RUN chown -R ${APP}.${APP} ${APP_BASE}/${APP}
USER ${APP}

# Initial build: needed to deploy the image as an standalone application.
# During development, it's useful to install the Python virtualenv.
RUN ${APP_BASE}/${APP}/scripts/build

# Use the Lektor default HTTP port
EXPOSE 5000

# The entrypoint for the development mode
ENTRYPOINT ["scripts/server"]

# This reduces the image size, but without this folder the container startup
# will take longer when running in development mode ("lektor server") as the
# ENTRYPOINT.
#RUN rm -rf /home/${APP}/.virtualenvs/onion-support-landing-page

FROM landing AS apache

# Include Apache
USER root
RUN apt-get update && apt-get install -y apache2 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the environment for Apache
# In Debian it won't suffice to set some of these as environment variables:
# they should be included at /etc/apache2/envvars instead.
RUN echo "export APACHE_RUN_USER=${APP}"                                                 >> /etc/apache2/envvars
RUN echo "export APACHE_RUN_GROUP=${APP}"                                                >> /etc/apache2/envvars
RUN echo "export APACHE_LOG_DIR=${APP_BASE}/${APP}/log"                                  >> /etc/apache2/envvars
RUN echo "export APACHE_LOCK_DIR=${APP_BASE}/${APP}/lock"                                >> /etc/apache2/envvars
RUN echo "export APACHE_RUN_DIR=${APP_BASE}/${APP}/run"                                  >> /etc/apache2/envvars
RUN echo "export APACHE_PID_FILE=${APP_BASE}/${APP}/pid/apache2.pid"                     >> /etc/apache2/envvars
RUN echo -n "<Directory ${APP_BASE}/${APP}/public>\nAllowOverride All\n</Directory>\n"    > /etc/apache2/conf-available/allow_override.conf
RUN echo -n "<Directory ${APP_BASE}/${APP}/public>\nOptions +Includes\n</Directory>\n"    > /etc/apache2/conf-available/options_includes.conf
RUN echo -n "<Directory ${APP_BASE}/${APP}/public>\nRequire all granted\n</Directory>\n"  > /etc/apache2/conf-available/require.conf
RUN echo "ServerName ${APP}"                                                              > /etc/apache2/conf-available/servername.conf
RUN echo "DocumentRoot ${APP_BASE}/${APP}/public"                                         > /etc/apache2/conf-available/documentroot.conf
RUN echo "Listen 5000"                                                                    > /etc/apache2/conf-available/listen.conf
RUN a2enconf allow_override options_includes require servername documentroot listen

USER ${APP}

RUN mkdir -p log lock run pid

# Serve the statically built site
ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
