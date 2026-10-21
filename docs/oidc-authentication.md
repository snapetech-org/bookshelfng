# OpenID Connect sign-in

BookshelfNG supports OIDC as a browser sign-in method. Select **OpenID Connect** under **Settings → General → Security**, then configure the provider on the server. Ordinary providers use Authorization Code with PKCE; Apple uses its documented form-post flow without PKCE. Local form login, API keys, and the existing API authentication behavior remain available. This adapter follows the [cross-project OIDC contract](https://github.com/snapetech-org/seerrng/blob/main/docs/maintainers/oidc-cross-project-template.md).

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

### Sign in with Apple

Set `BOOKSHELF_OIDC_ISSUER_URL` to exactly `https://appleid.apple.com`, use
the Apple Services ID as `BOOKSHELF_OIDC_CLIENT_ID`, and set
`BOOKSHELF_OIDC_CLIENT_SECRET` to the signed client-secret JWT. Register the
exact HTTPS redirect URI `https://<public-host>/signin-oidc`. BookshelfNG
requests only `openid email`, uses `response_mode=form_post`, and omits PKCE for
Apple's documented web flow. Apple may encode `email_verified` as a boolean or
string; only `true` is admitted. Rotate the JWT before its six-month maximum
expiry. See Apple's [environment setup](https://developer.apple.com/documentation/signinwithapple/configuring-your-environment-for-sign-in-with-apple)
and [web authorization flow](https://developer.apple.com/documentation/signinwithapple/incorporating-sign-in-with-apple-into-other-platforms).
