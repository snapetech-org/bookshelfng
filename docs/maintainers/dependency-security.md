# Dependency security

BookshelfNG's final release updates its frontend toolchain and records how to
recheck both package ecosystems. Run the audits after dependency restore:

```sh
yarn audit
dotnet list src/Readarr.sln package --vulnerable --include-transitive
```

The final source branch resolves zero Yarn advisories and zero vulnerable
.NET package rows. The frontend resolutions in `package.json` address the
reported `ajv`, `colord`, `cross-spawn`, `yaml`, and `zod` advisories. The
project keeps the exact resolved versions in `yarn.lock`.

## `braces` parser depth limit

The `braces` package has no published upstream fix for
[GHSA-vfj7-8cjw-p6xm](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm).
The repository carries a local MIT-licensed copy of `braces` 3.0.3 under
`patches/braces`, installed as `3.0.4-snapetech.0` through the Yarn resolution.
Its parser rejects brace or parenthesis nesting deeper than 256 before it can
build an AST that exhausts the JavaScript call stack. This is a frontend build
and lint tool dependency, not an application runtime component.

`patches/braces/PATCH.md` records the change. When upstream publishes an
equivalent fix, remove the local copy and the `braces` resolution, regenerate
`yarn.lock`, then rerun `yarn audit`, the frontend build, and lint.

The complete security and dependency changes are included in the final
BookshelfNG release. The source-side transfer helper is documented in the
[BookshelfNG to ChaptarrNG migration guide](../migrate-from-bookshelfng-to-chaptarrng.md).
