# Analytics

Onion Launchpad supports a basic analytics gathering based on [Matomo][]:

1. The feature is *disabled* by default, and enabled only if some environment
   variables are set.
2. This feature, even with a better configuration in terms of privacy, could
   still be a point of collecting access data without passing to the Tor
   network for better anonymization. And also would rely on additional JavaScript
   code embedded in the landing page.
3. Services operators are be recommended to host the backend only behind an
   HTTPS proxy without IP logging (and without passing the source IP to the
   backend, so if there's any backend vulnerability it won't be possible to
   attackers to discover user's IP addresses). ___Or even better: leave the
   backend behind an Onion Service___.
4. There is also a [consent UX][] informing users what and how it's
   collected, and asking for authorization. No cookies reside in the
   client machine.
5. The analytics collection is bypassed entirely if the [Do Not Track][]
   configuration is set. Onion Launchpad respects this setting
   [even if it's considered deprecated][].

It's also worth noting that adversaries could attack the analytics system by:

0. Intercepting DNS Queries in the form of `myanalytics.example.org` that may
   disclose information:
    * That an analytics platform exists.
    * That the user is giving information to this platform.
1. Adding fake access data into the metrics system.
2. Censoring the analytics endpoint so the user browser cannot reach it in
   order to send access data.
3. DDoS'ing the analytics backend.
4. Exploiting vulnerabilities in the backend to extract data.

The analytics functionality is controlled by these environment variables:

* `LEKTOR_ANALYTICS`: when set to `1`, enables the analytics collection.
* `LEKTOR_ANALYTICS_BACKEND`: contains the base URL of the Matomo instance.
  Example: `https://myanalytics.example.org/`. Onion Launchpad will then point
   to both `https://myanalytics.example.org/matomo.js` and
  `https://myanalytics.example.org/matomo.php`.
* `LEKTOR_ANALYTICS_SITE_ID`: should be set to the Matomo `siteId` configured
   in the backend.
* `LEKTOR_ANALYTICS_LINK_TRACKING`: when set to 1, activates Matomo's
  `enableLinkTracking` setting, otherwise keep it off.
* `LEKTOR_ANALYTICS_BROWSER_DETECTION`: when set to 1, use Matomo's
  browser feature detection, otherwise enforces `disableBrowserFeatureDetection`.
  You might want to turn this on if your Matomo backend is too
  old, since [disabling of browser detection was implemented only recently][].
* `LEKTOR_ANALYTICS_PRIVACY_POLICY_URL`: an URL for the privacy policy, as per
  [best practices on analytics gathering][].
* `LEKTOR_ANALYTICS_BACKGROUND_COLOR`: the background color for the [consent UX][],
  in hexadecimal format (`ffffff`).

Check Matomo's [JavaScript Tracking Client][] documentation for details.

[Matomo]: https://matomo.org
[consent UX]: https://okthanks.com/blog/2021/5/14/clean-consent-ux
[Do Not Track]: https://en.wikipedia.org/wiki/Do_Not_Track
[even if it's considered deprecated]: https://developer.mozilla.org/en-US/docs/Web/API/navigator/doNotTrack
[JavaScript Tracking Client]: https://developer.matomo.org/api-reference/tracking-javascript
[disabling of browser detection was implemented only recently]: https://github.com/matomo-org/matomo/pull/18599
[best practices on analytics gathering]: https://matomo.org/blog/2018/04/how-should-i-write-my-privacy-notice-for-matomo-analytics-under-gdpr/
