# Assets for Project 145

## Naming conventions

### General

* Fields are separated by underlines (`_`).
* Language codes use [TPO's convention][]
* `${AGENCY}` name is optional.
* Always include an english version for a logo, even if that means just copying
  the filename from other translation. This step is needed so [Onion
  Launchpad][] can have a default fallback logo.

### Folders

Use either `${AGENCY}` or `${PROJECT}` to host the assets for a given site.

### Favicons

Use the following naming scheme for the icons:

    favicon_${AGENCY}_${PROJECT}.svg

### Logos

Use the following naming scheme for the logos:

    logo_${AGENCY}_${SITE}_${LANG_CODE}.svg

[TPO's convention]: https://gitlab.torproject.org/tpo/community/l10n/-/wikis/Localization-for-developers
[Onion Launchpad]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad
