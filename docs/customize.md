# Customizing

Several parts of the site are configured through environment variables during
the Lektor build.

## Example

The following command exemplifies how environment variables can be passed to
Onion Launchpad at build time:

```
LEKTOR_FOREGROUND_COLOR=FF0000 \
LEKTOR_BACKGROUND_COLOR=FF7700 \
LEKTOR_BUTTON_COLOR=3377FF \
LEKTOR_ONION_URL_LOCK_FILTER=FF0000 \
LEKTOR_ONION_URL='https://abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz123d.onion' \
LEKTOR_FAVICON='/custom/my-icon.svg' \
LEKTOR_LOGO_PATH='/custom/my-logo.png' \
lektor build
```

It's a long build command, but ideally would only be run by a script.

## General customizations

Some of these variables are:

* `LEKTOR_FOREGROUND_COLOR`: This is the foreground/main site color in RGB hexadecimal format (`FFFFFF`).
* `LEKTOR_BACKGROUND_COLOR`: This is the background/accent site color in RGB hexadecimal format.
* `LEKTOR_BUTTON_COLOR`: This is the button color in RGB hexadecimal format -
                         might be the same as the foreground.
* `LEKTOR_ONION_URL_LOCK_FILTER`: This is the color of the lock icon next to the onion URL in RGB
                                hexadecimal format (`FFFFFF`) or (`FFF`).
* `LEKTOR_ONION_URL`: This is the onion URL of the service.
* `LEKTOR_SERVICE_NAME`: This sets the service name / project title.
* `LEKTOR_SERVICE_URL`: Sets the regular (i.e, the non-onion) URL for the service.
* `LEKTOR_ASSET_REPOSITORY_URL`: The URL of a public Git repository with
                                 additional assets to be cloned into `assets/custom`, allowing customizations
                                 such as the logo and favicon.
* `LEKTOR_FAVICON`: The favicon path relative to the `assets` folder, such as `/custom/my-icon.svg`.
* `LEKTOR_LOGO_PATH`: The logo path relative to the `assets` folder, such as `/custom/my-logo.png`.
* `LEKTOR_DEFAULT_LANGUAGE`: The default language of the site, such as `en`.
* `LEKTOR_AVAILABLE_LANGUAGES`: Limit the available languages to a subset, such as `en am ar`.
                                Please note that English will always be enabled, even if not explicitly configured,
                                since it works as a base language for all other translations.

## Analytics customizations

Analytic-related variables are documented in a [specific section](analytics.md).

## Per-language customizations

The following settings can be applied in a per-language basis:

* `LEKTOR_SERVICE_NAME`: you can fine tune the service name using per-language
  environment variables, like the following:
    * `LEKTOR_SERVICE_NAME_EN`.
    * `LEKTOR_SERVICE_NAME_ES`.
    * `LEKTOR_SERVICE_NAME_FA_AF`.
    * `LEKTOR_SERVICE_NAME_FA`.
    * `LEKTOR_SERVICE_NAME_FR`.
    * `LEKTOR_SERVICE_NAME_RU`.
    * `LEKTOR_SERVICE_NAME_ZH_CN`.
    * `LEKTOR_SERVICE_NAME_ZH_TW`.

## Asset customization

As stated earlier, `LEKTOR_ASSET_REPOSITORY_URL` allows specifying public Git
repository with assets like logos and icons.

Localized assets can be automatically used by Onion Launchpad if they follow
the naming convention where the language code is the last field in the file
name, separated by underscores, like this:

    some_file_name_${LANG_CODE}.svg

where `${LANG_CODE}` is one of the language codes specified in the `LEKTOR_AVAILABLE_LANGUAGES`
variable.

Example:

* `LEKTOR_AVAILABLE_LANGUAGES="en am ar"`.
* `LEKTOR_LOGO_PATH="/custom/my-logo.png"`.
* `LEKTOR_ASSET_REPOSITORY_URL="https://git.example.org/onion-launchpad-assets.git"`.
* Localized logo files: `custom/my-logo_am.png` and `custom/my-logo_ar.png` hosted
  at the Git repository pointed by `LEKTOR_ASSET_REPOSITORY_URL`.

Onion Launchpad always defaults to the main logo defined by `LEKTOR_LOGO_PATH`
if there's no localized version.
