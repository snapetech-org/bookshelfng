# BookshelfNG Helm chart

**Legacy chart for existing BookshelfNG deployments.** ChaptarrNG `v0.9.977`
includes the BookshelfNG SQLite converter in its standard image. Draft
ChaptarrNG PR #131 now contains a source-only, fail-closed chart candidate at
[`charts/bookshelfng`](https://github.com/snapetech-org/chaptarrng/tree/codex/bookshelf-retirement-next-20261018/charts/bookshelfng)
that preserves this release's Kubernetes resource identities. It is not
published or accepted for production cutover: no installed PVC upgrade,
GitOps sync, or Helm rollback has been validated. Keep the current release,
PVC, and independent backup until the operator has reviewed the migration
guide and the retirement gates close. The legacy OCI chart remains unchanged.
See the
[migration guide](https://github.com/snapetech-org/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md)
and [channel status](https://github.com/snapetech-org/bookshelfng/blob/main/docs/maintainers/chaptarr-consolidation.md).

This chart runs BookshelfNG as one StatefulSet replica and persists `/config`
with a PVC. BookshelfNG's SQLite database must not be shared by multiple active
replicas. Each released chart is pinned to the Hardcover container digest
produced in the same release, keeping the chart and app version aligned.

Install a specific release from GHCR:

```sh
helm upgrade --install bookshelfng \
  oci://ghcr.io/snapetech/bookshelfng/bookshelfng \
  --version 0.4.21-20
```

For an existing Softcover deployment, keep its configuration and data backed
up until provider settings have been reviewed for ChaptarrNG. Use `values.yaml`
to configure storage, ingress, service type, resources, and Kubernetes environment values.
Reference Kubernetes Secrets through `extraEnv[].valueFrom` for credentials; do
not put provider tokens in Helm values committed to source.

The chart disables automatic ServiceAccount token mounting, uses the
RuntimeDefault seccomp profile, and disables container privilege escalation.
The image still starts its LinuxServer service supervisor as root before
dropping the BookshelfNG process to its service account; do not set
`runAsNonRoot` or `readOnlyRootFilesystem` without replacing that startup path
and providing writable runtime mounts. Use Kubernetes Secret references for
the optional `BOOKSHELF_SEERRNG_API_KEY` integration credential.

See the [full installation guide](https://github.com/snapetech-org/bookshelfng/blob/main/docs/standalone-install.md).
