# Deploying

## GitLab deployments

The `deploy-onion-launchpad-on-gitlab` allows for a semi-automated deployment
procedure on GitLab.

### Installation

0. Setup a GitLab account for the deployments. Make sure that this account is
   validated to run CI/CD jobs.
1. [Setup GitLab authentication][] for this account.
2. Install [python-gitlab](https://python-gitlab.readthedocs.io).
   For Debian, the package is [python3-gitlab](https://tracker.debian.org/pkg/python-gitlab).
3. [Configure python-gitlab][] by creating a `~/.python-gitlab.cfg` file. Use the provided
   [.python-gitlab.cfg.sample][] as example.

[Setup GitLab authentication]: https://docs.gitlab.com/ee/api/#authentication
[Configure python-gitlab]: https://python-gitlab.readthedocs.io/en/stable/cli-usage.html?highlight=configuration#configuration-files
[.python-gitlab.cfg.sample]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/configs/deploy/.python-gitlab.cfg.sample

### Configuration

Copy from the example provided by [Onion Launchpad][]:

    cp /path/to/onion-launchpad/configs/deploy/onion-launchpad-test.gitlab.io.ini
       gitlab/$somesite.gitlab.io.ini

Or copy from an existing configuration:

    cp gitlab/$agency/$someothersite.ini gitlab/$somesite.ini

Then ajust the settings:

    $EDITOR gitlab/$somesite.ini

### Deployment

First, manually create a new group on GitLab. Due to [abuse in the automated
group creation][], this step cannot be automated.

Then use the GitLab deployment script provided by [Onion Launchpad][]:

    /path/to/onion-launchpad/scripts/deploy-onion-launchpad-on-gitlab \
      gitlab/$somesite.gitlab.io.ini

[abuse in the automated group creation]: https://gitlab.com/gitlab-org/gitlab/-/issues/244345#note_1021388399

## GitHub deployments

The `deploy-onion-launchpad-on-github` allows for a semi-automated deployment
procedure on GitHub.

### Installation

0. Setup a GitHub account for the deployments.
1. [Setup GitHub access token][] for this account with the `repo` and `admin:org` scopes.
2. Install [PyGithub][] (the Debian package is [pygithub][]) and [GitPython][]
   ([python3-git][] Debian package).
3. Create a `~/.pygithub.cfg` file. Use the the provided [.pygithub.cfg.sample][] as example.

[Setup GitHub access token]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
[PyGithub]: https://github.com/PyGithub/PyGithub
[pygithub]: https://tracker.debian.org/pygithub
[GitPython]: https://gitpython.readthedocs.io/en/stable/index.html
[python3-git]: https://tracker.debian.org/python-git
[.pygithub.cfg.sample]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/configs/deploy/.pygithub.cfg.sample

### Configuration

Configuration is analogous to the GitLab procedure, but use the provided GitHub config sample instead:

    cp /path/to/onion-launchpad/configs/deploy/onion-launchpad-test.github.io.ini \
       gitlab/$somesite.github.io.ini

### Deployment

First, manually create a new organization on GitHub, as this step currently
cannot be automated.

Then use the GitLab deployment script provided by [Onion Launchpad][]:

    /path/to/onion-launchpad/scripts/deploy-onion-launchpad-on-github \
      gitlab/$somesite.github.io.ini
