# Self-hosting catalog deployment

These catalog definitions are legacy BookshelfNG entries. They do not migrate
existing app identities or stored data, and the appdata helper does not update
a catalog entry or image reference. The definitions below now point at the
final BookshelfNG `.71` image so existing users can reach the migration-158
source boundary. They are not the recommended target for new installations;
use ChaptarrNG. Moving an existing catalog entry to ChaptarrNG still needs a
tested handoff for its app identity, volumes, port, and rollback behavior. See
the [migration guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
and [channel status](https://github.com/snapetech-org/bookshelfng/blob/main/docs/maintainers/chaptarr-consolidation.md).

This directory is the source of truth for the Docker-based self-hosting
catalog submissions for BookshelfNG. The adapters use the public Docker Hub
image so new installations do not need a registry login.

## Current stable image

```text
docker.io/snapetech/bookshelfng:hardcover-v0.4.21.71
```

The image supports `linux/amd64` and `linux/arm64` and serves its web UI on
TCP port `8787`. Persist `/config`, mount the managed book and audiobook
library at `/books`, and mount the download destination at `/downloads` when a
download client shares that path.

The final `softcover-v0.4.21.71` tag is available for existing Goodreads-compatible
libraries. The platform-specific submissions prepared from this contract are
CasaOS / ZimaOS, Umbrel, TrueNAS, Cosmos, CapRover, Portainer, Co-op Cloud,
Cloudron, and StartOS. Unraid is maintained separately.
