# Localized environment variables

A plugin implementing basic localization using environment variables.

This plugin was specifically developed for [Onion Launchpad][], but may be used
with any [Lektor][] application relying on the environment variables.

[Onion Launchpad]: https://gitlab.torproject.org/tpo/onion-services/onion-launchpad
[Lektor]: https://www.getlektor.com

## Installing

1. Install [lektor-envvars][] in your project.

2. Drop the package into your lektor project's `packages/` directory, and run
   `lektor plugins reinstall`.

[lektor-envvars]: https://github.com/roadsideseb/lektor-envvars

## Configuring

This plugin operates with the following convention:

1. Each variable name can be translated to any language in use. As and
   example, you can have the `LEKTOR_SERVICE_NAME` to provide the default site
   name.

2. For each language you want the site name to be translated, set a
   corresponding `LEKTOR_SERVICE_NAME_${LANG_CODE}` environment variable, where
   `$LANG_CODE` format is hyphenized and in uppercase (`PT_PT` instead of `pt-PT`).

The exact place to set these variables depends on your setup, such as an `.env`
file of in a build script;

## Using

Use `envvars_localized('SERVICE_NAME', this.alt)` anywhere in your Jinja
template to have the localized site name.

This function will make the following lookups:

1. Try to resolve a service name via `LEKTOR_SERVICE_NAME_${LANG_CODE}`
   environment variable.

2. If the variable above is unset, the function fallback to the value of the
   `LEKTOR_SERVICE_NAME` environment variable, or an empty string (`''`).

## Customizing

This plugins uses the same [environment variable prefix configuration][]
implemented by the envvars plugin.

[environment variable prefix configuration]: https://github.com/roadsideseb/lektor-envvars#custom-prefixes-or-no-prefix

## License

This plugin is licensed under the Zero-clause BSD license. See
[LICENSE.md](LICENSE.md) for more information.
