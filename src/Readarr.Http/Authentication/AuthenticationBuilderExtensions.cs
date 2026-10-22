using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Diacritical;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.IdentityModel.Protocols.OpenIdConnect;
using Microsoft.IdentityModel.Tokens;
using NzbDrone.Core.Authentication;
using NzbDrone.Core.Configuration;

namespace Readarr.Http.Authentication
{
    public static class AuthenticationBuilderExtensions
    {
        private const string OidcOpenIdConnectScheme = "OidcOpenIdConnect";
        private const string UiAuthScheme = "UIAuth";
        private static readonly Regex CookieNameRegex = new Regex(@"[^a-z0-9]+", RegexOptions.Compiled | RegexOptions.IgnoreCase);

        public static AuthenticationBuilder AddApiKey(this AuthenticationBuilder authenticationBuilder, string name, Action<ApiKeyAuthenticationOptions> options)
        {
            return authenticationBuilder.AddScheme<ApiKeyAuthenticationOptions, ApiKeyAuthenticationHandler>(name, options);
        }

        public static AuthenticationBuilder AddBasic(this AuthenticationBuilder authenticationBuilder, string name)
        {
            return authenticationBuilder.AddScheme<AuthenticationSchemeOptions, BasicAuthenticationHandler>(name, options => { });
        }

        public static AuthenticationBuilder AddNone(this AuthenticationBuilder authenticationBuilder, string name)
        {
            return authenticationBuilder.AddScheme<AuthenticationSchemeOptions, NoAuthenticationHandler>(name, options => { });
        }

        public static AuthenticationBuilder AddExternal(this AuthenticationBuilder authenticationBuilder, string name)
        {
            return authenticationBuilder.AddScheme<AuthenticationSchemeOptions, NoAuthenticationHandler>(name, options => { });
        }

        public static bool IsOidcConfigured()
        {
            var issuer = Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_ISSUER_URL")?.Trim();
            var redirect = Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_REDIRECT_URI")?.Trim();
            var allowPrivate = string.Equals(
                Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_ALLOW_PRIVATE_ISSUER"),
                "true",
                StringComparison.OrdinalIgnoreCase);

            return !string.IsNullOrWhiteSpace(issuer) &&
                   !string.IsNullOrWhiteSpace(Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_CLIENT_ID")) &&
                   !string.IsNullOrWhiteSpace(Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_CLIENT_SECRET")) &&
                   Uri.TryCreate(issuer, UriKind.Absolute, out var issuerUri) &&
                   Uri.TryCreate(redirect, UriKind.Absolute, out var redirectUri) &&
                   !string.IsNullOrWhiteSpace(issuerUri.Host) && !string.IsNullOrWhiteSpace(redirectUri.Host) &&
                   issuerUri.UserInfo.Length == 0 && issuerUri.Query.Length == 0 && issuerUri.Fragment.Length == 0 &&
                   redirectUri.UserInfo.Length == 0 && redirectUri.Query.Length == 0 && redirectUri.Fragment.Length == 0 &&
                   (issuerUri.Scheme == Uri.UriSchemeHttps || (allowPrivate && issuerUri.Scheme == Uri.UriSchemeHttp)) &&
                   redirectUri.Scheme == Uri.UriSchemeHttps &&
                   redirectUri.AbsolutePath.EndsWith("/signin-oidc", StringComparison.Ordinal);
        }

        public static string GetOidcProviderHint()
        {
            var provider = Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_PROVIDER")?.Trim();
            return string.IsNullOrWhiteSpace(provider) ? "generic" : provider;
        }

        public static AuthenticationBuilder AddAppAuthentication(this IServiceCollection services)
        {
            services.AddOptions<CookieAuthenticationOptions>(AuthenticationType.Forms.ToString())
                .Configure<IConfigFileProvider>((options, configFileProvider) =>
                {
                    // Replace diacritics and replace non-word characters to ensure cookie name doesn't contain any valid URL characters not allowed in cookie names
                    var instanceName = configFileProvider.InstanceName;
                    instanceName = instanceName.RemoveDiacritics();
                    instanceName = CookieNameRegex.Replace(instanceName, string.Empty);

                    options.Cookie.Name = $"{instanceName}Auth";
                    options.AccessDeniedPath = "/login?loginFailed=true";
                    options.LoginPath = "/login";
                    options.ExpireTimeSpan = TimeSpan.FromDays(7);
                    options.SlidingExpiration = true;
                    options.ReturnUrlParameter = "returnUrl";
                });

            services.AddOptions<CookieAuthenticationOptions>(AuthenticationType.Oidc.ToString())
                .Configure<IConfigFileProvider>((options, configFileProvider) =>
                {
                    var instanceName = configFileProvider.InstanceName.RemoveDiacritics();
                    instanceName = CookieNameRegex.Replace(instanceName, string.Empty);
                    options.Cookie.Name = $"{instanceName}OidcAuth";
                    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
                    options.Cookie.HttpOnly = true;
                    options.Cookie.SameSite = SameSiteMode.Lax;
                    options.AccessDeniedPath = "/login?loginFailed=true";
                    options.LoginPath = "/login";
                    options.ExpireTimeSpan = TimeSpan.FromDays(7);
                    options.SlidingExpiration = true;
                    options.ReturnUrlParameter = "returnUrl";
                });

            services.AddOptions<OpenIdConnectOptions>(OidcOpenIdConnectScheme)
                .Configure((OpenIdConnectOptions options) => ConfigureOidcOptions(options));

            var authenticationBuilder = services.AddAuthentication()
                .AddNone(AuthenticationType.None.ToString())
                .AddExternal(AuthenticationType.External.ToString())
                .AddBasic(AuthenticationType.Basic.ToString())
                .AddCookie(AuthenticationType.Forms.ToString())
                .AddCookie(AuthenticationType.Oidc.ToString())
                .AddOpenIdConnect(OidcOpenIdConnectScheme, options =>
                {
                    options.SignInScheme = AuthenticationType.Oidc.ToString();
                    options.Authority = "https://example.invalid";
                    options.ClientId = "unconfigured";
                    options.ResponseType = OpenIdConnectResponseType.Code;
                    options.UsePkce = !IsAppleIssuer(options.Authority);
                })
                .AddPolicyScheme(UiAuthScheme, UiAuthScheme, options =>
                {
                    options.ForwardDefaultSelector = context =>
                    {
                        var config = context.RequestServices.GetService<IConfigFileProvider>();
                        if (config?.AuthenticationMethod != AuthenticationType.Oidc)
                        {
                            return config?.AuthenticationMethod.ToString() ?? AuthenticationType.None.ToString();
                        }

                        var instanceName = CookieNameRegex.Replace(
                            config.InstanceName.RemoveDiacritics(),
                            string.Empty);
                        return context.Request.Cookies.ContainsKey($"{instanceName}Auth")
                            ? AuthenticationType.Forms.ToString()
                            : AuthenticationType.Oidc.ToString();
                    };
                })
                .AddApiKey("API", options =>
                {
                    options.HeaderName = "X-Api-Key";
                    options.QueryName = "apikey";
                    options.AllowQueryString = false;
                })
                .AddApiKey("SignalR", options =>
                {
                    options.HeaderName = "X-Api-Key";
                    options.QueryName = "access_token";
                    options.AllowQueryString = true;
                });

            services.Configure<ApiKeyAuthenticationOptions>("API", options =>
            {
                options.AllowQueryString = !string.Equals(
                    Environment.GetEnvironmentVariable("BOOKSHELF_ALLOW_API_KEY_QUERY"),
                    "false",
                    StringComparison.OrdinalIgnoreCase);
            });

            return authenticationBuilder;
        }

        private static void ConfigureOidcOptions(OpenIdConnectOptions options)
        {
            var issuer = Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_ISSUER_URL")?.Trim();
            var isAppleIssuer = IsAppleIssuer(issuer);
            var clientId = Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_CLIENT_ID")?.Trim();
            var clientSecret = Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_CLIENT_SECRET");
            var redirectUri = Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_REDIRECT_URI")?.Trim();
            var allowedEmails = ParseOidcSet(Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_ALLOWED_EMAILS"));
            var allowedDomains = ParseOidcSet(Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_ALLOWED_EMAIL_DOMAINS"));
            var allowAnyVerifiedUser = string.Equals(
                Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_ALLOW_ANY_VERIFIED_USER"),
                "true",
                StringComparison.OrdinalIgnoreCase);
            var allowPrivateIssuer = string.Equals(
                Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_ALLOW_PRIVATE_ISSUER"),
                "true",
                StringComparison.OrdinalIgnoreCase);

            var configured = IsOidcConfigured();

            options.SignInScheme = AuthenticationType.Oidc.ToString();
            options.Authority = configured ? issuer : "https://example.invalid";
            options.ClientId = configured ? clientId : "unconfigured";
            options.ClientSecret = configured ? clientSecret : string.Empty;
            options.ResponseType = OpenIdConnectResponseType.Code;
            options.UsePkce = !isAppleIssuer;
            options.SaveTokens = false;
            options.GetClaimsFromUserInfoEndpoint = !isAppleIssuer;
            options.RequireHttpsMetadata = !allowPrivateIssuer;
            options.BackchannelHttpHandler = new OidcBackchannelHandler(allowPrivateIssuer);
            options.BackchannelTimeout = TimeSpan.FromSeconds(15);
            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidIssuer = configured ? issuer : "https://example.invalid",
                ValidateAudience = true,
                ValidAudience = configured ? clientId : "unconfigured",
                ValidateLifetime = true,
                RequireSignedTokens = true,
                NameClaimType = "user"
            };
            options.ClaimActions.MapUniqueJsonKey("email_verified", "email_verified");
            options.Scope.Clear();
            var configuredScopes = Environment.GetEnvironmentVariable("BOOKSHELF_OIDC_SCOPES");
            var scopes = isAppleIssuer
                ? new[] { "openid", "email" }
                : string.IsNullOrWhiteSpace(configuredScopes)
                ? new[] { "openid", "profile", "email" }
                : configuredScopes.Split(new[] { ',', ' ', '\t', '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries)
                    .Select(scope => scope.Trim())
                    .Distinct(StringComparer.OrdinalIgnoreCase)
                    .ToArray();
            if (!scopes.Contains("openid", StringComparer.OrdinalIgnoreCase))
            {
                scopes = new[] { "openid" }.Concat(scopes).ToArray();
            }

            if (!scopes.Contains("email", StringComparer.OrdinalIgnoreCase))
            {
                scopes = scopes.Concat(new[] { "email" }).ToArray();
            }

            foreach (var scope in scopes)
            {
                options.Scope.Add(scope);
            }

            options.CorrelationCookie.SameSite = isAppleIssuer ? SameSiteMode.None : SameSiteMode.Lax;
            options.NonceCookie.SameSite = isAppleIssuer ? SameSiteMode.None : SameSiteMode.Lax;
            options.CorrelationCookie.SecurePolicy = CookieSecurePolicy.Always;
            options.NonceCookie.SecurePolicy = CookieSecurePolicy.Always;
            if (configured)
            {
                options.Events.OnRedirectToIdentityProvider = context =>
                {
                    context.ProtocolMessage.RedirectUri = redirectUri;
                    if (isAppleIssuer)
                    {
                        context.ProtocolMessage.ResponseMode = OpenIdConnectResponseMode.FormPost;
                    }

                    return Task.CompletedTask;
                };
            }

            options.Events.OnTicketReceived = context =>
            {
                var principal = context.Principal;
                var identity = principal?.Identity as ClaimsIdentity;
                var email = principal?.FindFirst(ClaimTypes.Email)?.Value ?? principal?.FindFirst("email")?.Value;
                var verified = principal?.FindFirst("email_verified")?.Value;
                var issuerClaim = principal?.FindFirst("iss")?.Value;
                var subject = principal?.FindFirst("sub")?.Value ?? principal?.FindFirst(ClaimTypes.NameIdentifier)?.Value;
                var emailIsVerified = string.Equals(verified, "true", StringComparison.OrdinalIgnoreCase);
                var normalizedEmail = email?.Trim().ToLowerInvariant() ?? string.Empty;
                var at = normalizedEmail.LastIndexOf('@');
                var domain = string.Empty;
                if (at >= 0 && at < normalizedEmail.Length - 1)
                {
                    domain = normalizedEmail.Substring(at + 1);
                }

                var admitted = allowAnyVerifiedUser ||
                               (allowedEmails.Count > 0 && allowedEmails.Contains(normalizedEmail)) ||
                               (allowedDomains.Count > 0 && allowedDomains.Contains(domain));

                if (configMethodIsOidc(context) && identity != null && emailIsVerified && admitted &&
                    !string.IsNullOrWhiteSpace(issuerClaim) && !string.IsNullOrWhiteSpace(subject))
                {
                    if (!identity.HasClaim(c => c.Type == "user"))
                    {
                        identity.AddClaim(new Claim("user", normalizedEmail));
                    }

                    if (!identity.HasClaim(c => c.Type == "identifier"))
                    {
                        var identityKey = Encoding.UTF8.GetBytes(issuerClaim + "\0" + subject);
                        identity.AddClaim(new Claim("identifier", Convert.ToHexString(SHA256.HashData(identityKey)).ToLowerInvariant()));
                    }

                    if (!identity.HasClaim(c => c.Type == "oidc_issuer"))
                    {
                        identity.AddClaim(new Claim("oidc_issuer", issuerClaim));
                    }

                    if (!identity.HasClaim(c => c.Type == "oidc_subject"))
                    {
                        identity.AddClaim(new Claim("oidc_subject", subject));
                    }

                    if (!identity.HasClaim(c => c.Type == "AuthType"))
                    {
                        identity.AddClaim(new Claim("AuthType", AuthenticationType.Oidc.ToString()));
                    }

                    return Task.CompletedTask;
                }

                context.HandleResponse();
                context.Response.Redirect(context.HttpContext.Request.PathBase + "/login?oidcFailed=true");
                return Task.CompletedTask;
            };

            options.Events.OnRemoteFailure = context =>
            {
                context.HandleResponse();
                context.Response.Redirect(context.HttpContext.Request.PathBase + "/login?oidcFailed=true");
                return Task.CompletedTask;
            };
        }

        private static bool configMethodIsOidc(TicketReceivedContext context)
        {
            return context.HttpContext.RequestServices.GetService<IConfigFileProvider>()?.AuthenticationMethod == AuthenticationType.Oidc;
        }

        private static bool IsAppleIssuer(string issuer)
        {
            return string.Equals(issuer?.Trim(), "https://appleid.apple.com", StringComparison.Ordinal);
        }

        private static HashSet<string> ParseOidcSet(string raw)
        {
            return (raw ?? string.Empty)
                .Split(new[] { ',', ';', ' ', '\t', '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries)
                .Select(value => value.Trim().ToLowerInvariant())
                .Where(value => value.Length > 0)
                .ToHashSet(StringComparer.OrdinalIgnoreCase);
        }
    }
}
