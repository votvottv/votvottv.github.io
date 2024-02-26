# Customizing

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
