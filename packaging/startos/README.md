# StartOS submission packet

This is a legacy BookshelfNG submission, not a ChaptarrNG upgrade. The StartOS
package identity, data contract, and rollback path still need a tested bridge.
ChaptarrNG `v0.9.977` is published with the migration-158 SQLite converter;
the source on ChaptarrNG `main` also contains the historical SQLite migration
chain. Neither release supports an automatic StartOS handoff yet. This
submission still uses the BookshelfNG `.37` image and has no tested update to
ChaptarrNG. It does not change the StartOS package identity or stored data.
New installations should use ChaptarrNG. Keep existing BookshelfNG
installations in service until the package identity, data mounts, conversion,
and rollback have been accepted. See the [migration guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
and [channel status](https://github.com/snapetech-org/bookshelfng/blob/main/docs/maintainers/chaptarr-consolidation.md).

The compiled StartOS wrapper is published at
https://github.com/snapetech-org/bookshelfng-startos.

- Package ID: `bookshelfng`
- Image: `docker.io/snapetech/bookshelfng:hardcover-v0.4.21.37` (legacy package snapshot; final `.71` is available but this package was not updated)
- Web UI: TCP `8787`
- Persistent data: `/config`, `/books`, `/downloads`

The wrapper previously passed its SDK typecheck and `ncc` build. That does
not validate an upgrade from the BookshelfNG image to ChaptarrNG. Keep this
submission parked until the package identity, data mounts, conversion, and
rollback have a tested StartOS handoff.
