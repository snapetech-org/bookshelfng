## Runner policy — owner directive, 2026-11-03

GitHub-hosted runner minutes are available again. Use compatible GitHub-hosted
runners for build, test, scan, packaging and release jobs when their operating
system and architecture requirements are met. Preserve native OS and
architecture. Use private ephemeral JIT runners when a job needs private
network access, special hardware or storage, or explicit JIT validation. Do not
require private JIT solely because of the former organization-wide policy, and
do not treat missing private capacity as a blocker when a compatible hosted
runner is available.

Keep untrusted pull-request code isolated in a disposable environment without
secrets, with minimal permissions and restricted egress. Do not widen trusted
runner-group access to make untrusted code run. Preserve active builds and other
agents' work. Do not restart the broker while it owns running guests. Select a
runner route that fits the workload and trust requirements; rerunning an old
run uses its original workflow revision.

The shared inventory continues to govern private JIT jobs. For a private route,
verify source routing, broker policy, runner-group access and live capacity
before relying on it.

## Upstream source attribution

When BookshelfNG gathers or adapts an idea, report, discussion, patch, rejected
request, issue, or pull request from upstream Bookshelf/Readarr or Chaptarr,
update `UPSTREAM_ATTRIBUTION.md` and the user-facing changelog in the same
change. Record the originating upstream URL, the upstream author’s GitHub
handle, the kind of source, and the behavior brought into BookshelfNG. Say that
the person contributed or suggested it to the upstream project and that
BookshelfNG independently adapted, integrated, or verified it. Never imply
that the person contributed directly to, endorsed, or participated in this
fork.

Credit closed, unmerged, superseded, and rejected upstream records when their
code or ideas materially informed the fork. Before a release, audit every new
upstream reference in commits, release-note fragments, and changelog entries
for an author link and originating issue, PR, or commit link. Missing source
credit is a release-note defect and must be fixed before publication.

If an upstream record informs a maintained plan, migration/consolidation
review, partial implementation, or unresolved investigation, add it to a
clearly labeled planned/not-yet-shipped or reviewed-disposition section. Do
not present review evidence or unfinished work as a released feature.

