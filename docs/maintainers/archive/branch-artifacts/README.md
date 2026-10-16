# Preserved branch artifacts

`pr105-pnpm-lock.yaml.txt` is a verbatim copy of the untracked `pnpm-lock.yaml`
found in the detached `bookshelfng-pr105-current` worktree on 2026-10-16. It is
kept here to preserve that dirty worktree artifact as requested. It is not an
active dependency lockfile and no build or release workflow reads it. Yarn and
the tracked `yarn.lock` remain the frontend package manager and lockfile.

`unraid-template-transition-proposal.xml.txt` and
`unraid-ca-profile-transition-proposal.xml.txt` preserve the proposed Unraid
image handoff from the dirty transition worktree. They are archived as plain
text and are not active templates. The published BookshelfNG template keeps
the BookshelfNG image while the distribution bridge remains disabled.

`bookshelfng-transition-worktree-20261016.patch` records the staged, unstaged,
and conflict-stage changes from that dirty transition worktree. It is an inert
snapshot for review, not an apply-ready patch. Synced Unraid source files were
restored to their companion-repository versions; their proposed content is
preserved in the snapshot and the separate plain-text template artifacts.
