# Cloudron community package

This is a legacy BookshelfNG package. It does not switch an installed Cloudron
app to ChaptarrNG. The package identity, persistent volumes, and rollback need
a separate tested migration. ChaptarrNG `v0.9.972` includes a converter for
the supported migration-158 SQLite schema, but this package does not change
the app identity or image. New deployments should use ChaptarrNG. See the
[migration guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
and [channel status](https://github.com/snapetech-org/bookshelfng/blob/main/docs/maintainers/chaptarr-consolidation.md).

The Cloudron package uses the public Hardcover Docker Hub image and persists
`/config`, `/books`, and `/downloads`. Build it from this directory with the
Cloudron CLI, then publish the generated `CloudronVersions.json` URL as a
community app in a Cloudron dashboard. Cloudron does not require a central
catalog PR for community apps.

After the source PR is merged, the version metadata URL is:
https://raw.githubusercontent.com/snapetech-org/bookshelfng/main/packaging/cloudron/CloudronVersions.json
