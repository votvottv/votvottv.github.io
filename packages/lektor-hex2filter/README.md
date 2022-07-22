# hex2filter

Convert a hex color code into a CSS filter to change the color of SVGs. Now as a lektor plugin!

## Installing

Drop the package into your lektor project's `packages/` directory, and run `lektor plugins reinstall`. There are no additional dependencies.

## Using

Use `{{ generate_filter('abc') }}` anywhere in your jinja templates. The function will return a full css rule (`filter: <filters...>;`); if you want just the filters, use `{{ generate_filter('abcdef').lstrip('filter:').rstrip(';') }}`

Example:

```css
.onion-url-lock {
       transform: translateY(4px);
       {{ generate_filter(envvars('ONION_URL_LOCK_FILTER')) }}
       display: inline-block;
       background-image: url({{ 'onion-site-lock.svg' | asseturl }});
       width: 32px;
       height: 32px;
       background-repeat: no-repeat;
       background-size: contain;
     }
```

## License

This plugin is licensed under the Zero-clause BSD license. See [LICENSE.md](LICENSE.md) for more information.
