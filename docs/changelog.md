# Onion Launchpad ChangeLog

## 1.0.3 - Unreleased

* Migrate Onion Launchpad CI to Debian Bookworm ([#90][]).

* Building with standalone GitLab Runner [has been
  deprecated][gitlab-exec-deprecated].

[gitlab-exec-deprecated]: https://gitlab.com/gitlab-org/gitlab/-/issues/385235
[#90]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/issues/90

## 1.0.2 - 2024-12-02

* Various dependencies updates.

* Disabled the automatic GitLab releases due to an issue:
  somehow this is failing to include CI Templates, and hence
  unable to find some jobs. Example on [pipeline #161094][].

[pipeline #161094]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/pipelines/161094

## 1.0.1 - 2024-04-18

* Minor release, mainly to test automatic GitLab releases
  triggered by new Git tags.

* Properly adds this ChangeLog in the generate documentation
  and in the main project folder.

## 1.0.0 - 2024-04-17

* Initial release.
