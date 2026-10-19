# Keep stable container aliases in sync

BookshelfNG stable releases now publish the same Hardcover image to `:main`
and `:latest` in GHCR and Docker Hub. Main-branch builds use development tags,
so they cannot move either stable alias. The Unraid template follows `:latest`.
