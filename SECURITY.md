# Security policy

BookshelfNG `0.4.21.71` is the final public release. New BookshelfNG releases
are frozen while the migration and retirement gates in
[issue #144](https://github.com/snapetech-org/bookshelfng/issues/144) remain
open, so this version is not receiving routine security updates. Keep the
existing service running until the migration path is accepted; do not point
ChaptarrNG at its appdata or switch an installation based on an unpublished
candidate. See the current
[retirement status](docs/maintainers/chaptarr-consolidation.md) before any
cutover. Vulnerabilities affecting the maintained destination should also be
reported through the
[ChaptarrNG security policy](https://github.com/snapetech-org/chaptarrng/blob/main/SECURITY.md).

Report suspected vulnerabilities through GitHub's private vulnerability
reporting for this repository. If that feature is unavailable, contact a
repository maintainer privately through GitHub before public disclosure.
Include the affected version, deployment type, steps to reproduce, and impact.
Do not include live API keys, passwords, cookies, or unredacted logs in a
public issue.

BookshelfNG API keys grant access to the API. Use the restricted
`BOOKSHELF_SEERRNG_API_KEY` for SeerrNG when possible, keep credentials in a
secret manager, and rotate exposed values. Configure trusted proxy addresses
before relying on forwarded client IP or HTTPS headers.
