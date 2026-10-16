# Release-note fragments

For any user-facing change, add one structured fragment under `release-notes/` describing it. A
single fragment may cover related user-facing changes in the same pull request. Keep shipped fragments unchanged. Tagged
`main-v*` image builds validate the fragments and include them in the GitHub
Release and Discord announcement.

Use a short, user-facing description rather than an implementation detail:

```md
---
category: fixed
audience: users, operators
area: metadata
action: none
breaking: false
---
Hardcover book searches now make one batched detail request for their results, reducing API usage without changing the books shown.
```

The frontmatter captures release context:

- `category`: `added`, `changed`, `fixed`, `security`, `removed`, or `deprecated`.
- `audience`: `users`, `operators`, or `users, operators`.
- `area`: a lowercase slug such as `bookshelf`, `metadata`, or `release-pipeline`.
- `action`: the required upgrade or operating step, or `none` when no action is needed.
- `breaking`: `true` or `false`; breaking changes must include an action.

The body is the release-ready summary: say what changed and why it matters to
the audience. Keep it to 30-400 characters, start with a capitalized sentence,
and end with punctuation. Do not paste commit messages, logs, or implementation
details.

Fragments are append-only. Add a new file instead of changing one that has
already shipped. Preview the notes in a change with:

```bash
yarn release-notes:preview --base origin/main --head HEAD
```

For internal-only work, no fragment is needed. In a pull request, either select the internal-only
option in the template or put `release-note: none` on its own line in the description. When a
direct push or merge check reads commit messages, put the same marker on its own line in the
commit message.

BookshelfNG posts release announcements with the repository secret
`DISCORD_RELEASE_WEBHOOK`. Do not put the webhook URL in source files or
workflow logs.
