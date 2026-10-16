# BookshelfNG Helm chart

**Legacy chart for existing BookshelfNG deployments.** Do not use it for a new
installation. The ChaptarrNG candidate adds BookshelfNG migration to its
ordinary image, but that release and a BookshelfNG Helm chart handoff are not
published yet. Keep the existing release, PVC, and independent backup until a
chart-specific migration bridge is built and tested. The handoff must use the
same ChaptarrNG image as a fresh installation; no compatibility image is
maintained. See the
[migration status](https://github.com/snapetech/chaptarrng/blob/main/docs/MIGRATE_FROM_BOOKSHELFNG.md).

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
up until provider settings have been reviewed for ChaptarrNG. Use `values.yaml` to configure
storage, ingress, service type, resources, and Kubernetes environment values.
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
