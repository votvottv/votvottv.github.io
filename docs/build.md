# Building Onion Launchpad

There are some documented ways in how to setup your development or deployment
environment for this project:

0. Using a CI/CD system such as [GitLab CI/CD][].
1. Using [Docker][] and [Docker Compose][].
2. Using [GitLab Runner][].
3. Using [PyEnv][].
4. Setting up your environment manually.

They are explained in the following sections, and of course you can also proceed
with your own procedure if nothing else fits. They're tested with [Debian][]-like
operating systems.

The procedures can also be executed inside a virtual machine, preferably using
[Debian][].

[GitLab CI/CD]: https://docs.gitlab.com/ee/ci/
[Debian]: https://www.debian.org/

## Environment file

The `LEKTOR_*` and other environment variables can be stored in the `.env`
configuration file.

## Helper scripts

Also, number of helper scripts are available to aid development, testing and deployment:

* `scripts/provision-docker-compose`: installs [Docker Compose][] in a [Debian][]-based
  system.
* `provision-gitlab-runner`: installs [GitLab Runner][] in a [Debian][]-based system.
* `provision-pyenv`: install [PyEnv][] locally at user's `$HOME/.pyenv`.
* `provision`: setus up the basic system environment (system-wide packages).
* `env`: sets up the basic [Python][] environment needed to build the landing pages
  (local Python packages).
* `build`: the actual build script.
* `build-with-gitlab-runner`: build the landing page using [GitLab Runner][].
* `server`: wrapper around [lektor server](https://www.getlektor.com/docs/cli/server/).
* `server-public`: basic HTTP server used to inspect build artifacts stored at
  the `public/` folder.

[Python]: https://www.python.org

## Using a CI/CD system such as [GitLab CI/CD][]

For [GitLab CI/CD][] we provide two configurations:

1. [.gitlab-ci.yml][]: the standard CI/CD used when the project
   is hosted at https://gitlab.torproject.org.
2. [.gitlab-ci-deployment.yml][]: the CI/CD configuration
   when the repository is hosted in other GitLab instances.

[.gitlab-ci.yml]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/.gitlab-ci.yml
[.gitlab-ci-deployment.yml]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/.gitlab-ci-deployment.yml

## Using [Docker][] and [Docker Compose][]

Make sure you have [Docker][] and [Docker Compose][] properly installed.
The [provision-docker-compose][] script serves
as an example in how to do that.

[provision-docker-compose]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/scripts/provision-docker-compose?ref_type=heads

Then proceed as usual:

    docker-compose up

This should build the container image and bring a service container running
`lektor server` with a HTTP server listening at [http://localhost:5000][].

As an alternative, it's possible to use the [provided Dockerfile][Dockerfile]
for serving a statically built landing page.

[Docker]: https://docs.docker.com
[Docker Compose]: https://docs.docker.com/compose
[http://localhost:5000]: http://localhost:5000

## Using [GitLab Runner][]

!!! note Deprecation notice

    This method [has been deprecated][gitlab-exec-deprecated].

The [GitLab Runner][] approach is aimed to test the [CI configuration for
deployment][] directly through a [GitLab Runner][]
instance locally installed in your computer.

Install [GitLab Runner][] according to the [docs](https://docs.gitlab.com/runner/install/)
or using the provided [provision-gitlab-runner][] script.

Then proceed running the corresponding build script:

    scripts/build-with-gitlab-runner

If the build is successful, the resulting site will be available at the `public/` folder
and can be browser using a HTTP server such the one provided by this repository which
listens on [http://localhost:5000][]:

    scripts/server-public

[gitlab-exec-deprecated]: https://gitlab.com/gitlab-org/gitlab/-/issues/385235
[GitLab Runner]: https://docs.gitlab.com/runner
[provision-gitlab-runner]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/scripts/provision-gitlab-runner
[CI configuration for deployment]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/.gitlab-ci-deployment.yml

## Using [PyEnv][]

Another approach is to use [PyEnv][] to setup your environment with the required
[Python][] version needed to build the landing page.

The [provision-pyenv][] script has an example in how to
do that, which should run after the [provision script][].

    scripts/provision
    scripts/provision-pyenv

Then you can simply use the provided [build script][]:

    scripts/build

You can also manually invoke [Lektor][] like this:

    source scripts/env
    lektor clean --yes
    lektor server

The [virtualenv][] is created by default inside of your `$HOME/.virtualenvs`
folder, but that can be customized with the `$VENV` shell environment variable.

[PyEnv]: https://github.com/pyenv/pyenv
[virtualenv]: https://docs.python.org/3/library/venv.html
[provision-pyenv]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/scripts/provision-pyenv
[provision script]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/scripts/provision
[build script]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/scripts/build

## Setting up your environment manually

You might use this approach if you prefer a customized way to install the
required [Python][] version and/or you already have your own [Lektor][]
workflow.

First install the required [Python][] version, whose exact number can be found
in the [Dockerfile][] or at the [.gitlab-ci-deployment.yml][] file.

A suggested way is running this command sequence:

    lektor-venv && source .env && lektor clean --yes && lektor server

where `lektor-venv` is a [bash][] function that sets up a `venv`, and `.env` is
literally just a file exporting the `LEKTOR_*` environment variables:


```shell
lektor-venv ()
{
    VENV="${VENV:-$HOME/.virtualenvs/onion-launchpad}

    [ -d "$VENV" ] && source "$VENV/bin/activate" && \
      echo 'virtualenv found in "$VENV" and activated' && return;

    python3.8 -m venv "$VENV" && source "$VENV/bin/activate" && \
      pip install --upgrade pip lektor && echo 'virtualenv set up in "$VENV" and activated'
}
```

Make sure to:

* Replace `python3.8` with the required [Python][] version, if needed.
* Set the `$VENV` shell environment variable according to your preference.

[Lektor]: https://www.getlektor.com
[bash]: https://www.gnu.org/software/bash
[Dockerfile]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/Dockerfile
