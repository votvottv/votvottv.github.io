# Onion Launchpad security

## Threat model

An Onion Launchpad landing page is a regular site providing information
about how to connect to a specific [Onion Service][].

In contexts of internet censorship, it can offer alternative ways to connect to
a web site that also have enhanced privacy guarantees. By relying on
[collateral freedom][], service operators can host landing pages in providers
that are "too big to block".

Since it's safe to assume that an user accessing such a landing page is
probably not using the Tor Browser (since the user is looking for ways to
accessing a given blocked site), we cannot assume that the user has set all the
privacy protections offered by Tor Browser.

That's a chicken-and-egg problem: in order to give users the power to access
content more safely, the landing pages (or any other portal like a Tor Browser
download page) cannot offer user all access safeguards without leaking some
information like the landing page address. So there are inherent trade-offs
during this "bootstrap phase".

There are known risks and they can be minimized, but to do that it's important
to consider a threat model not just of anonymized metrics collection but also
from the landing page usage in general.

In a broader sense, accessing a landing pages for Onion Services also involves
the following:

0. Knowing the landing page address beforehand.

1. Making a DNS query asking for the IP address where the landing page is hosted:
    * DNS queries to the provider can be intercepted by an attacker, as they're usually
      not encrypted.
      * That may:
          * Leak that the user is trying to access a given landing page (and hence
            can be inferred that the user is trying to bypass censorship).
          * Allow for censoring the landing page at the DNS level.
          * Allowing for attackers to provide the IP address of a fake landing
            page without HTTPS.
      * Mitigations:
          * Use DNS-over-HTTPS or DNS-over-TLS, but it cannot be assumed that the
            user has these in place.
          * Host the landing page only in a path from an existing platform, such
            as https://example.net/the-landing-page instead of
            https://the-landing-page.example.net, but that do not protect against
            tampering the DNS response, but only from censors discovering the landing
            page address.
          * Use a VPN to access the landing page, but an user doing this may already
            be able to access the service.

2. Making a TLS connection to the IP address where the landing page is hosted:
    * The client connection will use a Server Name Indicator (SNI) during the
      handshake process.
      * That may:
          * Leak that the user is trying to access a given landing page (and hence
            can be inferred that the user is trying to bypass censorship).
          * Allow for censoring the landing page by dropping the TLS handshake
            connection.
      * Mitigations:
          * Use ECH (Encrypted Client Hello), but that is not yet a standard,
            widely deployed or available for production systems.
          * Host the landing page only at a path from an existing platform, such
            as https://example.net/the-landing-page instead of
            https://the-landing-page.example.net.
          * Use a VPN to access the landing page, but an user doing this may already
            be able to access the service.

The following attack surface should also be considered:

3. HTTP downgrade, where an attacker can prevent the connection to the landing
   page be upgrade to HTTPS.
    * That may:
        * Allow attackers to inject arbitrary content to the landing page, which
          may lead the user to download non-official, malicious versions of Tor Browser
          and/or to offer the wrong .onion address for the service.
    * Mitigations:
        * Recent changes in browsers that don't allow unencrypted HTTP connections,
          which my be widely deployed these days.
        * Always provide the link to the landing page with `https://`.

4. Landing page censorship:
    * Mitigations:
        * Provide many landing page mirrors using the [collateral freedom][]
          approach and inform the user about each available option.

5. Data retention: the hosting provider may have a retention policy that keeps
   data with IP addresses stored for long periods.
    * That may:
        * Allow for adversaries to request (or hack, if they can) to these logs
          to get user-identifiable information.
    * Mitigations:
        * It may be hard for providers to comply with requests for disclosing read
          access to a landing page given that this usually don't break any law
          in the jurisdiction the page is hosted.

Conclusions:

1. In general, landing pages hosted with custom subdomains are not an ideal
   solution for places where there's not just censorship but also persecution
   of persons that tries to bypass it.

2. If the scenario is only general censorship, accessing landing pages using
   HTTPS usually won't add any additional harm to the user and the trade-off is
   smaller.

[Onion Service]: https://community.torproject.org/onion-services
[collateral freedom]: https://bypass.censorship.guide/user/index.html
