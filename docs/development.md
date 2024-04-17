# Development

Onion Launchpad development guidelines and workflow are listed here.

## Release procedure

Release cycle workflow.

### Version update

Set the version number:

    ONION_LAUNCHPAD_VERSION=1.0.0

### Register the changes

Update the ChangeLog:

    $EDITOR ChangeLog

Commit and tag:

    git diff # review
    git commit -a -m "Feat: Onion Launchpad $ONION_LAUNCHPAD_VERSION"
    git tag -s $ONION_LAUNCHPAD_VERSION -m "Onion Launchpad $ONION_LAUNCHPAD_VERSION"

Push changes and tags. Example:

    git push origin        && git push upstream
    git push origin --tags && git push upstream --tags

Once a tag is pushed, a [GitLab release][] is created.

[GitLab release]: https://docs.gitlab.com/ee/user/project/releases/
