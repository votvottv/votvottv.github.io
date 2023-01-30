# Onion Launchpad

The Onion Launchpad is a customizable [lego](https://gitlab.torproject.org/tpo/web/lego) landing page for organizations and individuals to advertise their onion addresses to their audiences. The landing page is easy to navigate and describes to users how to connect to an Onion Service.

The landing page offers [localized](https://www.transifex.com/otf/tor-onion-support/dashboard/) content about how to download [Tor Browser](https://www.torproject.org/download/), connect to the Tor network, and access an Onion Service.

It's a statically built website that can be easily deployed.

Check the [**live demo**](https://tpo.pages.torproject.net/onion-services/onion-launchpad/)!

- More on Onion Services: https://community.torproject.org/onion-services/
- Localization at Tor: https://gitlab.torproject.org/tpo/community/l10n/-/wikis/Localization-for-developers
- Tor Browser manual: https://tb-manual.torproject.org/

## Dependencies

This project relies on [Lektor](https://www.getlektor.com/)
and some dependencies detailed at the
[TPA CI templates](https://gitlab.torproject.org/tpo/tpa/ci-templates) project.

A [provision script](scripts/provision) is available as an example of dependency
installation from a [Debian][] stable system, and can be adapted to your own environment
and needs.

[Debian](https://www.debian.org)

## Building

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

### Using a CI/CD system such as [GitLab CI/CD][]

For [GitLab CI/CD][] we provide two configurations:

1. [.gitlab-ci.yml][.gitlab-ci.yml]: the standard CI/CD used when the project
   is hosted at https://gitlab.torproject.org.
2. [.gitlab-ci-deployment.yml][.gitlab-ci-deployment.yml]: the CI/CD configuration
   when the repository is hosted in other GitLab instances.

### Using [Docker][] and [Docker Compose][]

Make sure you have [Docker][] and [Docker Compose][] properly installed.
The [provision-docker-compose](scripts/provision-docker-compose) script serves
as an example in how to do that.

Then proceed as usual:

    docker-compose up

This should build the container image and bring a service container running
`lektor server` with a HTTP server listening at [http://localhost:5000][].

As an alternative, it's possible to use the [provided Dockerfile][Dockerfile]
for serving a statically built landing page.

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

## Customizing

Several parts of the site are configured through environment variables during
the Lektor build. These variables are:

- `LEKTOR_FOREGROUND_COLOR`: This is the foreground/main site color in RGB hexadecimal format (`ffffff`).
- `LEKTOR_BACKGROUND_COLOR`: This is the background/accent site color in RGB hexadecimal format.
- `LEKTOR_BUTTON_COLOR`: This is the button color in RGB hexadecimal format -
                         might be the same as the foreground.
- `LEKTOR_ONION_URL_LOCK_FILTER`: This is the color of the lock icon next to the onion URL in RGB
                                hexadecimal format (ffffff) or (fff).
- `LEKTOR_ONION_URL`: This is the onion URL of the service.
- `LEKTOR_SERVICE_NAME`: This sets the service name / project title.
- `LEKTOR_SERVICE_URL`: Sets the regular (i.e, the non-onion) URL for the service.
- `LEKTOR_ASSET_REPOSITORY_URL`: The URL of a public Git repository with
                                 additional assets to be cloned into `assets/custom`, allowing customizations
                                 such as the logo and favicon.
- `LEKTOR_FAVICON`: The favicon path relative to the `assets` folder, such as `/custom/my-icon.svg`.
- `LEKTOR_LOGO_PATH`: The logo path relative to the `assets` folder, such as `/custom/my-logo.png`.
- `LEKTOR_DEFAULT_LANGUAGE`: The default language of the site, such as `en`.
- `LEKTOR_AVAILABLE_LANGUAGES`: Limit the available languages to a subset, such as `en am ar`.
                                Please note that english will always be enabled, even if not explicitly configured,
                                since it works as a base language for all other translations.

An example build command would like something like the following:

```
LEKTOR_FOREGROUND_COLOR=FF0000 \
LEKTOR_BACKGROUND_COLOR=FF7700 \
LEKTOR_BUTTON_COLOR=3377FF \
LEKTOR_ONION_URL_LOCK_FILTER=FF0000 \
LEKTOR_ONION_URL='https://abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz1234.onion' \
LEKTOR_FAVICON='/custom/my-icon.svg' \
LEKTOR_LOGO_PATH='/custom/my-logo.png' \
lektor build
```

It's a long build command, but ideally would only be run by a script.
See below for examples.

## Deploying

### GitLab deployments

The `deploy-onion-launchpad-on-gitlab` allows for a semi-automated deployment
procedure on GitLab.

#### Installation

0. Setup a GitLab account for the deployments. Make sure that this account is
   validated to run CI/CD jobs.
1. [Setup GitLab authentication][] for this account.
2. Install [python-gitlab](https://python-gitlab.readthedocs.io).
   For Debian, the package is [python3-gitlab](https://tracker.debian.org/pkg/python-gitlab).
3. [Configure python-gitlab][] by creating a `~/.python-gitlab.cfg` file.

[Setup GitLab authentication]: https://docs.gitlab.com/ee/api/#authentication
[Configure python-gitlab]: https://python-gitlab.readthedocs.io/en/stable/cli-usage.html?highlight=configuration#configuration-files

#### Configuration

Copy from the example provided by [Onion Launchpad][]:

    cp /path/to/onion-launchpad/configs/deploy/onion-launchpad-test.gitlab.io.ini
       gitlab/$somesite.gitlab.io.ini

Or copy from an existing configuration:

    cp gitlab/$agency/$someothersite.ini gitlab/$somesite.ini

Then ajust the settings:

    $EDITOR gitlab/$somesite.ini

#### Deployment

First, manually create a new group on GitLab. Due to [abuse in the automated
group creation][], this step cannot be automated.

Then use the GitLab deployment script provided by [Onion Launchpad][]:

    /path/to/onion-launchpad/scripts/deploy-onion-launchpad-on-gitlab \
      gitlab/$somesite.gitlab.io.ini

[abuse in the automated group creation]: https://gitlab.com/gitlab-org/gitlab/-/issues/244345#note_1021388399

### GitHub deployments

The `deploy-onion-launchpad-on-github` allows for a semi-automated deployment
procedure on GitHub.

#### Installation

0. Setup a GitHub account for the deployments.
1. [Setup GitHub access token][] for this account with the `repo` and `admin:org` scopes..
2. Install [PyGithub][] (the Debian package is [pygithub][]) and [GitPython][]
   ([python3-git][] Debian package).
3. Create a `~/.pygithub.cfg` file. Use the the provided [.pygithub.cfg.sample][] as example.

[Setup GitHub access token]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
[PyGithub]: https://github.com/PyGithub/PyGithub
[pygithub]: https://tracker.debian.org/pygithub
[GitPython]: https://gitpython.readthedocs.io/en/stable/index.html
[python3-git]: https://tracker.debian.org/python-git
[.pygithub.cfg.sample]: configs/deploy/.pygithub.cfg.sample

#### Configuration

Configuration is analogous to the GitLab procedure, but use the provided GitHub config sample instead:

    cp /path/to/onion-launchpad/configs/deploy/onion-launchpad-test.github.io.ini \
       gitlab/$somesite.github.io.ini

#### Deployment

First, manually create a new group on GitHub, as this step currently cannot be
automated.

Then use the GitLab deployment script provided by [Onion Launchpad][]:

    /path/to/onion-launchpad/scripts/deploy-onion-launchpad-on-github \
      gitlab/$somesite.github.io.ini

## Adding a new RTL language

If you end up enabling translation support for a right-to-left (RTL) language,
be sure to add the language's ISO 639-1/ISO 639-3 codes (add both if the
language has both) to the `rtl` list in `databags/alternatives.json`:

```json
{
    "rtl": [..., ISO 639 code here, ...]
}
```

The `page.html` template uses this databag to decide if the page should be
displayed as RTL. If your new RTL language isn't in the databag, it will be
rendered "mirrored" to how it should be, like left-to-right languages are.

## Threat model

An Onion Launchpad landing page is a regular site providing information
about how to connect to a specific [Onion Service][].

In contexts of internet censorship, it can offer alternative ways to connect to
a web site that also have enhanced privacy guarantees. By relying on
[collateral freedom][], service operators can host landing pages in providers
that are "too big to block".

Since it's safe to assume that an user accessing such a landing page is
probably not using the Tor Browser (since the user is looking for ways to
accessing a given blocked site), we cannot assume that the user has set all the
privacy protections offered by Tor Browser.

That's a chicken-and-egg problem: in order to give users the power to access
content more safely, the landing pages (or any other portal like a Tor Browser
download page) cannot offer user all access safeguards without leaking some
information like the landing page address. So there are inherent trade-offs
during this "bootstrap phase".

There are known risks and they can be minimized, but to do that it's important
to consider a threat model not just of anonymized metrics collection but also
from the landing page usage in general.

In a broader sense, accessing a landing pages for Onion Services also involves
the following:

0. Knowing the landing page address beforehand.

1. Making a DNS query asking for the IP address where the landing page is hosted:
    * DNS queries to the provider can be intercepted by an attacker, as they're usually
      not encrypted.
      * That may:
          * Leak that the user is trying to access a given landing page (and hence
            can be inferred that the user is trying to bypass censorship).
          * Allow for censoring the landing page at the DNS level.
          * Allowing for attackers to provide the IP address of a fake landing
            page without HTTPS.
      * Mitigations:
          * Use DNS-over-HTTPS or DNS-over-TLS, but it cannot be assumed that the
            user has these in place.
          * Host the landing page only in a path from an existing platform, such
            as https://example.net/the-landing-page instead of
            https://the-landing-page.example.net, but that do not protect against
            tampering the DNS response, but only from censors discovering the landing
            page address.
          * Use a VPN to access the landing page, but an user doing this may already
            be able to access the service.

2. Making a TLS connection to the IP address where the landing page is hosted:
    * The client connection will use a Server Name Indicator (SNI) during the
      handshake process.
      * That may:
          * Leak that the user is trying to access a given landing page (and hence
            can be inferred that the user is trying to bypass censorship).
          * Allow for censoring the landing page by dropping the TLS handshake
            connection.
      * Mitigations:
          * Use ECH (Encrypted Client Hello), but that is not yet a standard,
            widely deployed or available for production systems.
          * Host the landing page only at a path from an existing platform, such
            as https://example.net/the-landing-page instead of
            https://the-landing-page.example.net.
          * Use a VPN to access the landing page, but an user doing this may already
            be able to access the service.

The following attack surface should also be considered:

3. HTTP downgrade, where an attacker can prevent the connection to the landing
   page be upgrade to HTTPS.
    * That may:
        * Allow attackers to inject arbitrary content to the landing page, which
          may lead the user to download non-official, malicious versions of Tor Browser
          and/or to offer the wrong .onion address for the service.
    * Mitigations:
        * Recent changes in browsers that don't allow unencrypted HTTP connections,
          which my be widely deployed these days.
        * Always provide the link to the landing page with `https://`.

4. Landing page censorship:
    * Mitigations:
        * Provide many landing page mirrors using the [collateral freedom][]
          approach and inform the user about each available option.

5. Data retention: the hosting provider may have a retention policy that keeps
   data with IP addresses stored for long periods.
    * That may:
        * Allow for adversaries to request (or hack, if they can) to these logs
          to get user-identifiable information.
    * Mitigations:
        * It may be hard for providers to comply with requests for disclosing read
          access to a landing page given that this usually don't break any law
          in the jurisdiction the page is hosted.

Conclusions:

1. In general, landing pages hosted with custom subdomains are not an ideal
   solution for places where there's not just censorship but also persecution
   of persons that tries to bypass it.

2. If the scenario is only general censorship, accessing landing pages using
   HTTPS usually won't add any additional harm to the user and the trade-off is
   smaller.

[Onion Service]: https://community.torproject.org/onion-services
[collateral freedom]: https://bypass.censorship.guide/user/index.html

## Analytics

Onion Launchpad supports a basic analytics gathering based on [Matomo][]:

1. The feature is *disabled* by default, and enabled only if some environment
   variables are set.
2. This feature, even with a better configuration in terms of privacy, could
   still be a point of collecting access data without passing to the Tor
   network for better anonymization. And also would rely on additional JavaScript
   code embedded in the landing page.
3. Services operators are be recommended to host the backend only behind an
   HTTPS proxy without IP logging (and without passing the source IP to the
   backend, so if there's any backend vulnerability it won't be possible to
   attackers to discover user's IP addresses). ___Or even better: leave the
   backend behind an Onion Service___.
4. There is also a [consent UX][] informing users what and how it's
   collected, and asking for authorization. No cookies reside in the
   client machine.
5. The analytics collection is bypassed entirely if the [Do Not Track][]
   configuration is set. Onion Launchpad respects this setting
   [even if it's considered deprecated][].

It's also worth noting that adversaries could attack the analytics system by:

0. Intercepting DNS Queries in the form of `myanalytics.example.org` that may
   disclose information:
    * That an analytics platform exists.
    * That the user is giving information to this platform.
1. Adding fake access data into the metrics system.
2. Censoring the analytics endpoint so the user browser cannot reach it in
   order to send access data.
3. DDoS'ing the analytics backend.
4. Exploiting vulnerabilities in the backend to extract data.

The analytics functionality is controlled by these environment variables:

* `LEKTOR_ANALYTICS`: when set to `1`, enables the analytics collection.
* `LEKTOR_ANALYTICS_BACKEND`: contains the base URL of the Matomo instance.
  Example: `https://myanalytics.example.org/`. Onion Launchpad will then point
   to both `https://myanalytics.example.org/matomo.js` and
  `https://myanalytics.example.org/matomo.php`.
* `LEKTOR_ANALYTICS_SITE_ID`: should be set to the Matomo `siteId` configured
   in the backend.
* `LEKTOR_ANALYTICS_LINK_TRACKING`: when set to 1, activates Matomo's
  `enableLinkTracking` setting, otherwise keep it off.
* `LEKTOR_ANALYTICS_BROWSER_DETECTION`: when set to 1, use Matomo's
  browser feature detection, otherwise enforces `disableBrowserFeatureDetection`.
  You might want to turn this on if your Matomo backend is too
  old, since [disabling of browser detection was implemented only recently][].

Check Matomo's [JavaScript Tracking Client][] documentation for details.

[Matomo]: https://matomo.org
[consent UX]: https://okthanks.com/blog/2021/5/14/clean-consent-ux
[Do Not Track]: https://en.wikipedia.org/wiki/Do_Not_Track
[even if it's considered deprecated]: https://developer.mozilla.org/en-US/docs/Web/API/navigator/doNotTrack
[JavaScript Tracking Client]: https://developer.matomo.org/api-reference/tracking-javascript
[disabling of browser detection was implemented only recently]: https://github.com/matomo-org/matomo/pull/18599
