# Sponsor 123 Landing Page

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

## Adding a new RTL language

If you end up enabling translation support for a right-to-left (RTL) language, be sure to add the language's ISO 639-1/ISO 639-3 codes (add both if the language has both) to the `rtl` list in `databags/alternatives.json`:

```json
{
    "rtl": [..., ISO 639 code here, ...]
}
```

The `page.html` template uses this databag to decide if the page should be displayed as RTL. If your new RTL language isn't in the databag, it will be rendered "mirrored" to how it should be, like left-to-right languages are.
