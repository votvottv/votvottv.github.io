# Sponsor 123 Landing Page

## Dependencies

This project relies on [Lektor](https://www.getlektor.com/)
and some dependencies detailed at the
[TPA CI templates](https://gitlab.torproject.org/tpo/tpa/ci-templates) project.

A [provision script](scripts/provision) is available as an example of dependency
installation from a [Debian][] stable system, and can be adapted to your own environment
and needs.

[Debian](https://www.debian.org)

## Building

Several parts of the site are configured through environment variables during the lektor build. These variables are:

- `LEKTOR_FOREGROUND_COLOR`: This is the foreground/main site color in RGB hexadecimal format (`ffffff`)
- `LEKTOR_BACKGROUND_COLOR`: This is the background/accent site color in RGB hexadecimal format
- `LEKTOR_BUTTON_COLOR`: This is the button color in RGB hexadecimal format - it's the same as the foreground for RFERL, but none of the others
- `LEKTOR_ONION_URL_LOCK_FILTER`: This is a CSS filter that converts a black SVG to a different color. You can calculate the filter using [this codepen tool](https://codepen.io/sosuke/pen/Pjoqqp)
- `LEKTOR_ONION_URL`: This is the onion URL of the service

An example build command would like something like the following:

```
LEKTOR_FOREGROUND_COLOR=FF0000 LEKTOR_BACKGROUND_COLOR=FF7700 LEKTOR_BUTTON_COLOR=3377FF LEKTOR_ONION_URL_LOCK_FILTER='invert(57%) sepia(50%) saturate(5826%) hue-rotate(162deg) brightness(96%) contrast(101%);' LEKTOR_ONION_URL='https://abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz1234.onion' lektor b
```

It's a long build command, but ideally would only be run by a script.
An [example script](scripts/build) is provided which calls `lektor` after ensuring
additional dependencies are installed (see below).

## Adding a new RTL language

If you end up enabling translation support for a right-to-left (RTL) language, be sure to add the language's ISO 639-1/ISO 639-3 codes (add both if the language has both) to the `rtl` list in `databags/alternatives.json`:

```json
{
    "rtl": [..., ISO 639 code here, ...]
}
```

The `page.html` template uses this databag to decide if the page should be displayed as RTL. If your new RTL language isn't in the databag, it will be rendered "mirrored" to how it should be, like left-to-right languages are.

## Developing

There are some documented ways in how to setup your development environment for
this project:

1. Using [Docker][] and [Docker Compose][].
2. Using [GitLab Runner][].
3. Using [PyEnv][].
4. Setting up your environment manually.

They are explained in the following sections, and of couse you can also proceed
with your own procedure if nothing else fits. They're tested with [Debian][]-like
operating systems.

The procedures can also be executed inside a virtual machine, preferably using
[Debian][].

### Environment file

The `LEKTOR_*` and other environment variables can be stored in the `.env`
configuration file.

### Helper scripts

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

### Using [Docker][] and [Docker Compose][]

Make sure you have [Docker][] and [Docker Compose][] properly installed.
The [provision-docker-compose](scripts/provision-docker-compose) script serves
as an example in how to do that.

Then proceed as usual:

    docker-compose up

This should build the container image and bring a service container running
`lektor server` with a HTTP server listening at [http://localhost:5000][].

[Docker]: https://docs.docker.com
[Docker Compose]: https://docs.docker.com/compose
[http://localhost:5000]: http://localhost:5000

### Using [GitLab Runner][]

The [GitLab Runner][] approach is aimed to test the [CI configuration for
deployment](.gitlab-ci-deployment.yml) directly through a [GitLab Runner][]
instance locally installed in your computer.

Install [GitLab Runner][] according to the [docs](https://docs.gitlab.com/runner/install/)
or using the provided [provision-gitlab-runner](scripts/provision-gitlab-runner) script.

Then proceed running the corresponding build script:

    scripts/build-with-gitlab-runner

If the build is successful, the resulting site will be available at the `public/` folder
and can be browser using a HTTP server such the one provided by this repository which
listens on [http://localhost:5000][]:

    scripts/server-public

[GitLab Runner]: https://docs.gitlab.com/runner

### Using [PyEnv][]

Another approach is to use [PyEnv][] to setup your environment with the required
[Python][] version needed to build the landing page.

The [provision-pyenv](scripts/provision-pyenv) script has an example in how to
do that, which should run after the [provision](scripts/provision) script:

    scripts/provision
    scripts/provision-pyenv

Then you can simply use the provided [build](scripts/build) script:

    scripts/build

You can also manually invoke [Lektor][] like this:

    source scripts/env
    lektor clean --yes
    lektor server

The [virtualenv][] is created by default inside of your `$HOME/.virtualenvs`
folder, but that can be customized with the `$VENV` shell environment variable.

[PyEnv]: https://github.com/pyenv/pyenv
[virtualenv]: https://docs.python.org/3/library/venv.html

### Setting up your environment manually

You might use this approach if you prefer a customized way to install the
required [Python][] version and/or you already have your own [Lektor][]
workflow.

First install the required [Python][] version, whose exact number can be found
in the [Dockerfile](Dockerfile) or at the [.gitlab-ci-deployment](.gitlab-ci-deployment)
file.

A suggested way is running this command sequence:

    lektor-venv && source .env && lektor clean --yes && lektor server

where `lektor-venv` is a [bash][] function that sets up a `venv`, and `.env` is
literally just a file exporting the `LEKTOR_*` environment variables:


```shell
lektor-venv ()
{
    VENV="${VENV:-$HOME/.virtualenvs/onion-support-landing-page}

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
