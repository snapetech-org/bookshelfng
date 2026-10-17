# SnapeTech MCP

BookshelfNG does not run an MCP server inside the application. The shared
`snapetech-mcp` process reads its existing book API over MCP stdio transport.
Its quickstart is in the sibling `snapetech-mcp/README.md`.

## Tools and API access

| MCP tool | BookshelfNG endpoint | Result |
| --- | --- | --- |
| `bookshelfng_status` | `GET /api/v1/system/status` | Reachability only. |
| `bookshelfng_list_books` | `GET /api/v1/book/paged` | Bounded projected page. The mediaType query authenticates the key, but the controller does not filter records by it. |
| `bookshelfng_search_authors` | `GET /api/v1/author/lookup` | Bounded author metadata search; provider results are not guaranteed to be format-filtered. |
| `bookshelfng_search_book_catalog` | `GET /api/v1/book/lookup` | Bounded book catalog search; provider results are not guaranteed to be format-filtered. |
| `bookshelfng_get_book_history` | `GET /api/v1/history` | Bounded history for a caller-supplied book ID; the mediaType query is an auth gate, not a result filter. |

Use the dedicated `BOOKSHELF_SEERRNG_API_KEY`, supplied through a container or
orchestrator secret. Configure `SNAPETECH_MCP_APPS=bookshelfng`,
`SNAPETECH_MCP_BOOKSHELFNG_URL=<BookshelfNG base URL>`,
`SNAPETECH_MCP_BOOKSHELFNG_API_KEY=<integration key>`, and
`SNAPETECH_MCP_BOOKSHELFNG_MEDIA_TYPE=ebook` or `audiobook` in the MCP host's
protected environment. The bridge sends the key in `X-Api-Key` and includes the
required `mediaType` query value on every API call. One MCP process is configured for
one media type so the matching integration key can authenticate; this query is not a
reliable record-level format boundary.

When moving this connection to ChaptarrNG, replace the BookshelfNG app and
media-type environment variables with the ChaptarrNG app, URL, and dedicated
service key described in the
[ChaptarrNG MCP guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/integrations/snapetech-mcp.md).
The full handoff steps are in the
[BookshelfNG migration guide](../migrate-from-bookshelfng-to-chaptarrng.md#install-channel-notes-and-support-limits).

## Credential and data boundaries

The SeerrNG integration key is restricted to book-related routes and requires a
mediaType query, but it can add or update authors and books. That query is an
authentication gate: source review found that /api/v1/book/paged does not itself
filter records by format, and the history route is book-ID scoped rather than
media-type scoped. Do not treat this key or MCP process as an ebook/audiobook data
isolation boundary. The adapter only issues GET requests and excludes file paths,
provider credentials, release names, and raw event data. Use a dedicated key and rotate
it if exposed.

Keep the process attached to a trusted local client. Prefer HTTPS for remote
instances and never expose the stdio server through a TCP bridge or reverse
proxy.

## Competitor feature coverage

BookshelfNG is a book acquisition and library manager. Its [capability map](../capabilities-and-compatibility.md) covers
author/book monitoring, indexer RSS, manual and missing-book search, download-client
integration, import/rename/upgrade, multiple formats on one book, and multiple metadata
sources. [Calibre-Web](https://github.com/janeczku/calibre-web) and [Audiobookshelf](https://github.com/advplyr/audiobookshelf) are adjacent reader/server products with
browsing, in-browser reading or streaming, collections, user progress, device delivery,
and podcast workflows; they are not direct substitutes for the acquisition engine.

Snapetech MCP exposes book pages, author/catalog search, and book-scoped history. Search
can contact configured providers. Queue is omitted because its route is not reliably
filtered by media type. The existing paged-book and history routes also do not establish
a type-specific record boundary, so the configured media type must not be presented as
data isolation. Book additions, queue controls, import/move, renaming, and download
actions remain a separate write-capability review.

**Confidence:** high for the linked feature summaries and checked key/controller behavior; moderate for direct comparison because Calibre-Web and Audiobookshelf focus on reading and listening workflows.

Source contract: `SECURITY.md`,
`src/Readarr.Http/Authentication/ApiKeyAuthenticationHandler.cs`,
`src/NzbDrone.Host/SeerrIntegrationPathMiddleware.cs`, and
`src/Readarr.Api.V1/openapi.json`.
