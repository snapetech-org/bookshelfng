# Cloudron community package

This is a legacy BookshelfNG package. It does not switch an installed Cloudron
app to ChaptarrNG. The package identity, persistent volumes, and rollback need
a separate tested migration; do not use it for new deployments during the
retirement transition. See the
[migration status](https://github.com/snapetech/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md).

The Cloudron package uses the public Hardcover Docker Hub image and persists
`/config`, `/books`, and `/downloads`. Build it from this directory with the
Cloudron CLI, then publish the generated `CloudronVersions.json` URL as a
community app in a Cloudron dashboard. Cloudron does not require a central
catalog PR for community apps.

After the source PR is merged, the version metadata URL is:
https://raw.githubusercontent.com/snapetech/bookshelfng/main/packaging/cloudron/CloudronVersions.json
