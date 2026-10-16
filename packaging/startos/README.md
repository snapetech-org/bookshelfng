# StartOS submission packet

This is a legacy BookshelfNG submission, not a ChaptarrNG upgrade. The StartOS
package identity, data contract, and rollback path still need a tested bridge.
ChaptarrNG `v0.9.972` includes a converter for the supported migration-158
SQLite schema, but this submission does not change its package identity or
image. See the [migration guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
and [channel status](https://github.com/snapetech-org/bookshelfng/blob/main/docs/maintainers/chaptarr-consolidation.md).

The compiled StartOS wrapper is published at
https://github.com/snapetech-org/bookshelfng-startos.

- Package ID: `bookshelfng`
- Image: `docker.io/snapetech/bookshelfng:hardcover-v0.4.21.37`
- Web UI: TCP `8787`
- Persistent data: `/config`, `/books`, `/downloads`

The wrapper passes the current Start9 SDK typecheck and `ncc` build. Start9's
marketplace submission is a human-gated review: send the wrapper repository URL
and this source repository to `submissions@start9labs.com`, including the
license and runtime-port details above.
