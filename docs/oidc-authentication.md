# OpenID Connect sign-in

BookshelfNG supports OIDC as a browser sign-in method. Select **OpenID Connect** under **Settings → General → Security**, then configure the provider on the server. Ordinary providers use Authorization Code with PKCE; Apple uses its documented form-post flow without PKCE. Local form login, API keys, and the existing API authentication behavior remain available. This adapter follows the [cross-project OIDC contract](https://github.com/snapetech-org/seerrng/blob/main/docs/maintainers/oidc-cross-project-template.md).

For the complete list of provider IDs, issuer examples, official setup pages,
and scope/claim caveats, see the shared
[provider catalog](https://github.com/snapetech-org/seerrng/blob/main/docs/maintainers/oidc-provider-catalog.md).

Set these environment variables for the BookshelfNG process:

```dotenv
BOOKSHELF_OIDC_ISSUER_URL=https://id.example.com/realms/books
BOOKSHELF_OIDC_CLIENT_ID=bookshelfng
BOOKSHELF_OIDC_CLIENT_SECRET=replace-with-the-client-secret
BOOKSHELF_OIDC_REDIRECT_URI=https://books.example.com/signin-oidc
BOOKSHELF_OIDC_ALLOWED_EMAILS=operator@example.com
BOOKSHELF_OIDC_PROVIDER=keycloak
```

`BOOKSHELF_OIDC_PROVIDER` is an optional display hint. The login screen uses a
local icon and direct official setup link for `google`, `microsoft-entra`,
`okta`, `auth0`, `keycloak`, `authentik`, `zitadel`, `amazon-cognito`,
`gitlab`, `fusionauth`, `onelogin`, `pingone`, `jumpcloud`, or `apple-sign-in`.
Unknown values use generic OIDC presentation;
discovery and issuer validation continue to use `BOOKSHELF_OIDC_ISSUER_URL`.

The redirect URI must be the exact HTTPS URL registered with the provider and must end in `/signin-oidc`. If BookshelfNG is served below a URL base path, include that path in the registered redirect URI. Ordinary providers use `openid profile email`; Apple is forced to `openid email`. The app validates the provider ID token on the server and requires `email_verified=true`.

By default, only exact addresses or domains in `BOOKSHELF_OIDC_ALLOWED_EMAILS` and `BOOKSHELF_OIDC_ALLOWED_EMAIL_DOMAINS` can sign in. Address and domain lists are combined. With no allowlist, access is denied. `BOOKSHELF_OIDC_ALLOW_ANY_VERIFIED_USER=true` explicitly admits any identity with a verified email claim.

Optional settings:

| Variable | Default | Purpose |
| --- | --- | --- |
| `BOOKSHELF_OIDC_SCOPES` | `openid profile email` | Additional scopes; `openid` and `email` are always requested. |
| `BOOKSHELF_OIDC_PROVIDER` | `generic` | Login label/icon/setup link hint; does not change OIDC validation. |
| `BOOKSHELF_OIDC_ALLOWED_EMAIL_DOMAINS` | empty | Comma or whitespace separated verified email domains. |
| `BOOKSHELF_OIDC_ALLOW_ANY_VERIFIED_USER` | `false` | Allows any verified email to sign in. |
| `BOOKSHELF_OIDC_ALLOW_PRIVATE_ISSUER` | `false` | Allows a private issuer endpoint to use HTTP. Keep the browser callback on HTTPS. |

OIDC sign-in creates the normal BookshelfNG authentication cookie. The browser never receives provider tokens. Group claims do not grant roles. Local form login remains available for recovery when OIDC is misconfigured.

## Enable, verify, and recover

Create a confidential web client and register only the exact HTTPS URL ending
`/signin-oidc`. If BookshelfNG is served below a base path, include that path in
`BOOKSHELF_OIDC_REDIRECT_URI` and in the provider registration. Set the issuer,
client ID, secret, redirect URI, and admission policy through the server-side
configuration. Keep the secret in a protected deployment environment or
secret store; never put it in a browser setting or a checked-in file.

Select **OpenID Connect** under **Settings → General → Security** after the
provider values are ready. Verify one admitted and one denied verified email,
then confirm the expected BookshelfNG authentication cookie and local
authorization behavior. Test a local form login and API key as recovery before
relying on OIDC. Provider groups do not grant local roles, and email does not
automatically link a separate local account.

To disable OIDC, choose the intended local authentication method in the
security settings and remove or clear the server-side OIDC provider values.
Apply the deployment configuration using its usual restart/reload process.
Rotate a provider secret at both ends and repeat the allowed/denied sign-in
checks after the new value takes effect.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Provider reports a callback mismatch | Confirm the exact public HTTPS URL ends in `/signin-oidc`; include the reverse-proxy base path and match scheme, host, port, and trailing slash. |
| Discovery or token validation fails | Compare the configured issuer exactly with the discovery `issuer`; check provider tenant/realm, DNS, CA trust, and outbound access. Use private issuer access only for a trusted internal IdP. |
| A verified user is denied | Confirm the ID token or UserInfo contains email and affirmative `email_verified`; check exact addresses, domains, and provider-side claim release. An empty allow-list denies by default. |
| Callback state or cookie is missing | Start a new login at the public hostname, keep the browser session/cookies, and confirm the reverse proxy forwards the external HTTPS scheme and host. |
| Sign-in works but permissions are wrong | Review BookshelfNG's local user authorization; provider groups do not assign roles and email does not merge accounts. |
| Apple form-post is rejected | Verify the Services ID, Apple issuer, `/signin-oidc`, `openid email`, signed client-secret JWT, HTTPS origin, and cross-site Secure cookie behavior. |

For support, include BookshelfNG's version, provider ID, redacted issuer host,
callback path, and timestamp. Redact authorization codes, client secrets,
tokens, and raw claims.

## Sign in with Apple

Set `BOOKSHELF_OIDC_ISSUER_URL` to exactly `https://appleid.apple.com`, use
the Apple Services ID as `BOOKSHELF_OIDC_CLIENT_ID`, and set
`BOOKSHELF_OIDC_CLIENT_SECRET` to the signed client-secret JWT. Register the
exact HTTPS redirect URI `https://<public-host>/signin-oidc`. BookshelfNG
requests only `openid email`, uses `response_mode=form_post`, and omits PKCE for
Apple's documented web flow. Apple may encode `email_verified` as a boolean or
string; only `true` is admitted. Rotate the JWT before its six-month maximum
expiry. See Apple's [environment setup](https://developer.apple.com/documentation/signinwithapple/configuring-your-environment-for-sign-in-with-apple)
and [web authorization flow](https://developer.apple.com/documentation/signinwithapple/incorporating-sign-in-with-apple-into-other-platforms).
