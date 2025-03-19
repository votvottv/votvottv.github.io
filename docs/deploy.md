# Deploying Onion Launchpad

## GitLab deployments

### Automated GitLab deployments

The `deploy-onion-launchpad-on-gitlab` allows for a semi-automated deployment
procedure on GitLab. It works both for the official
[GitLab.com](https://gitlab.com) and other instances.

#### Installation

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

#### Configuration

Copy from the example provided by [Onion Launchpad][]:

    cp /path/to/onion-launchpad/configs/deploy/onion-launchpad-test.gitlab.io.ini
       gitlab/$somesite.gitlab.io.ini

Or copy from an existing configuration:

    cp gitlab/$agency/$someothersite.ini gitlab/$somesite.ini

Then adjust the settings:

    $EDITOR gitlab/$somesite.ini

[Onion Launchpad]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad

#### Deployment

First, manually create a new group on GitLab. Due to [abuse in the automated
group creation][], this step cannot be automated.

Then use the GitLab deployment script provided by [Onion Launchpad][]:

    /path/to/onion-launchpad/scripts/deploy-onion-launchpad-on-gitlab \
      gitlab/$somesite.gitlab.io.ini

[abuse in the automated group creation]: https://gitlab.com/gitlab-org/gitlab/-/issues/244345#note_1021388399

### Triggering a build on GitLab

Follow these steps to manually trigger an Onion Launchpad pipeline at some
GitLab mirror (requires privileges at the mirror repository):

1. Go to the mirror repository, like `https://gitlab.com/${group}/${group}.gitlab.io`.
2. Then go to CI/CD -> Pipelines, `https://gitlab.com/${group}/${group}.gitlab.io/-/pipelines`.
3. Click on "Run pipeline" or go directly to `https://gitlab.com/${group}/${group}.gitlab.io/-/pipelines/new`.
4. Click on "Run pipeline" again to execute.

Then you can follow the build log for unexpected errors, but in general the
build should be successful and the landing page will be updated at
[`https://${group}.gitlab.io`.

## GitHub deployments

Onion Launchpad comes with a [GitHub action for landing page deployment][] that
triggers on repository changes and also maintains a scheduled rebuild.

[GitHub action for landing page deployment]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/.github/workflows/gh-pages.yml

### Automated GitHub deployments

The `deploy-onion-launchpad-on-github` allows for a semi-automated deployment
procedure on [GitHub][].

[GitHub]: https://github.com

#### Installation

0. Setup a [GitHub][] account for the deployments.
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

#### Configuration

Configuration is analogous to the GitLab procedure, but use the provided [GitHub][] config sample instead:

    cp /path/to/onion-launchpad/configs/deploy/onion-launchpad-test.github.io.ini \
       gitlab/$somesite.github.io.ini

#### Deployment

First, manually create a new organization on [GitHub][], as this step currently
cannot be automated.

Then use the GitLab deployment script provided by [Onion Launchpad][]:

    /path/to/onion-launchpad/scripts/deploy-onion-launchpad-on-github \
      gitlab/$somesite.github.io.ini

### Manual repository creation

If you prefer to manually create an Onion Launchpad repository fork on
[GitHub][], proceed as follows:

* Log into [GitHub][] using your project's user.
* [Create a free organization](https://github.com/organizations/plan).
* Create an empty repository under this organization:
  * At `https://github.com/organizations/${organization}/repositories/new`,
    where `${organization` is the organization name you just created.
  * Named as `${organization}.github.io`.
  * Make sure to let the repository visibility set to "public".
  * Do not initialize the repository.

Now you just need to push Onion Launchpad code to this remote:

    cd /path/to/onion-launchpad
    git remote add organization git@github.com:${organization}/${organization}.github.io.git
    git push organization main

### Triggering a build on GitHub

Follow these steps to manually trigger an Onion Launchpad pipeline at some
GitHub mirror (requires privileges at the mirror repository):

1. Go to the mirror repository, like `https://github.com/${organization}/${organization}.github.io`.
2. Then go to Actions, `https://github.com/${organization}/${organization}.github.io/actions`.
3. Select the "GitHub Pages" action.
4. Click on the "Run workflow" button and click again the inner "Run workflow" button.

Then you can follow the build log for unexpected errors, but in general the
build should be successful and the landing page will be updated at
`https://${organization}.github.io`.

### Setting up a mirror on GitHub

The [GitHub action for landing page deployment][] can also be used together
with GitLab to [GitHub][] mirroring, triggering landing page builds for all
commits added to the `main` branch.

The following example assumes you have admin access at the [Onion Launchpad
upstream repository][], but you can easily adapt to whatever GitLab repository
you're using as the Onion Launchpad mirror origin.

[Onion Launchpad upstream repository][]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/

* Start by adding a new mirror on the [GitLab repository settings][]:
  * Git repository URL: `ssh://git@github.com/${organization}/${organization}.github.io.git`.
  * Mirror direction: push.
  * Input or detect host keys.
  * Authentication method: SSH public key.
  * Mirror only protected branches.
  * Click on "Mirror repository".
  * The mirror will appear in a listing below the form. Click on the clipboard
    icon to copy the generate SSH public key for this mirror into your
    clipboard.
* On [GitHub keys config page](https://github.com/settings/keys):
  * Add a new SSH key, pasting the SSH public key into the form.
* On `https://github.com/${organization}/${organization}.github.io/settings/secrets/actions`:
  * Add a new repository secrets for each environment variable.
* Again on [GitLab repository settings][]:
  * Click on the refresh button of this mirror to do the initial push into the
    remote [GitHub][] repository.
* On `https://github.com/${organization}/${organization}.github.io/actions`:
  * Manually trigger the "[GitHub][] Pages" workflow to build the landing page for
    the first time.
  * Check that the [GitHub][] page branch (`gh-pages`) is automatically built after
    the workflow runs.
* On `https://github.com/${organization}/${organization}.github.io/settings/pages`:
  * Set the pages source branch to `gh-pages`.
* Again on `https://github.com/${organization}/${organization}.github.io/actions`:
  * Watch for the `pages-build-deployment` workflow.

Now your landing page mirror should be accessible via `http://${organization}.github.io`.

[GitLab repository settings]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/settings/repository
