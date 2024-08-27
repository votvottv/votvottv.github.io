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

### Announcement

Announce the new release:

* Post a message to the [Tor Forum][], using the [onion-launchpad-announce tag][].
* Send a message to the [tor-announce][] mailing list ONLY in special cases,
  like important security issues.

Template:

```
Subject: [RELEASE] Onion Launchpad [security] release $ONION_LAUNCHPAD_VERSION

Greetings,

We just released Onion Launchpad $ONION_LAUNCHPAD_VERSION, a tool for testing and
monitoring the status of Onion Services:
https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/docs/upgrading.md

[This release fixes a security issue. Please upgrade as soon as possible!]

[This release requires a database migration for those using the monitoring node:]
[https://gitlab.torproject.org/tpo/onion-services/onion-launchpad/-/blob/main/docs/upgrading.md]

# ChangeLog

$CHANGELOG
```

[tor-announce]: https://lists.torproject.org/cgi-bin/mailman/listinfo/tor-announce
[Tor Forum]: https://forum.torproject.org
[onion-launchpad-announce tag]: https://forum.torproject.org/tag/onion-launchpad-announce
