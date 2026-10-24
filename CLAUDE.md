# CLAUDE.md

Guidance for Claude Code in this repository: **Taihei Mihon** (`dev.taihei::taihei-mihon`), a
cross-platform fake-data generator for Scala 3 on the JVM and Scala.js in many languages and
scripts, the successor of taihei-lorem 4.x. Part of the Taihei Framework; the family's rules come
from the parent folder's `CLAUDE.md` when this repo is checked out under `~/Projects/Taihei`.

## Commands

```bash
make validate          # repo-guard, release and data-check tests, scalafix, scalafmt, compile, test, MiMa and budget, JVM and JS
make budget            # size budget: data per language and in all, JVM jar, Scala.js fixture
make repo-guard        # Maven Central only: no other repository, every dev.taihei pin on Central
make mima              # binary compatibility with the newest 5.x release tag on Maven Central
make test              # ./mill __.test.testForked (JS tests run under Node)
make publish-dry-run   # the bundle Maven Central would receive, written to out/
make release-prepare TYPE=patch|minor|major EMBARGO=0|1   # then review RELEASE_x_y_z.md;
                       # EMBARGO=1 when the ticket has the label embargo (read it with fude first)
make release-finalize  # GitHub Packages and the read-back: only with the maintainer's yes
make release-github    # after the push: the bundle on an immutable GitHub Release
```

Releases follow ADR 0003: one signed bundle, uploaded unchanged to this repository's GitHub
Packages registry, read back, tagged and pushed, kept on an immutable GitHub Release, and taken
to Maven Central by the next release train in nakama. A security fix (`EMBARGO=1`) goes to
Central first with `make publish`. The publish token lives in `~/.taihei-packages-publish.env`,
the read token in Coursier's credentials file; never read or print either.

## Layout

- `shared/src/dev/taihei/mihon/`: `Mihon` (a class bound to one language, created by `seeded` or
  `secure`), `Person`, `Address`, `Gender`, `SampleImages`; the internal data model in `data/`
  and the small internal lists in `sources/`.
- `shared/resources/dev/taihei/mihon/data/`: the language data, the only copy. The JVM reads it
  from the classpath; for Scala.js the build generates `EmbeddedData` from it, after checking
  every file against its schema (`EmbeddedData` in `build.mill`).
- `scripts/data/`: the scripts that build the data (`python3 scripts/data/build.py <tag>`), never
  run by the build; downloads go to a cache outside the repo and are recorded with their SHA-256
  in `scripts/data/sources.lock.json`. Sources and licences: `docs/data-sources.md` and NOTICE.
  A new source needs the CISO's licence ruling before its data is committed.
- `jvm/src/…` and `js/src/…`: the platform `ResourceLoader`.
- `shared/test/src/…`: zio-test specs, run on both platforms. `SeededSpec` pins a seed's values
  per language, `LanguagesSpec` the conventions of each language, `DataSpec` that both platforms
  load exactly the files on disk. A change to the data or a draw updates `SeededSpec`.
- `budget/src/`: the Scala.js fixture of the size budget, never published.
- `docs/skill/`: the API reference for the library's Claude Code skill.

## Rules

- Whatever is in `shared/` compiles on Scala.js: no JVM-only API there.
- No global generator and no wall clock: every draw goes through the instance's `Random`, using
  only `nextInt`, `nextInt(n)`, `nextLong`, `nextBoolean` and `nextDouble`, so a seed gives the
  same values on both platforms.
- The public API is `Mihon`, `Person`, `Address`, `Gender` and `SampleImages`; everything else is
  `private[mihon]`. It follows semantic versioning; a break is a major release with a migration
  section in the README.
- Every dependency comes from Maven Central under an Apache-compatible licence; the build needs no
  credentials. taihei-tsuji is pinned in `V.taiheiTsuji` and released first.
- Data is generic (common names, real cities, words, MIME types), every piece from a source named
  in `docs/data-sources.md` under an Apache-compatible licence: nothing taken from a client or a
  person, nothing CC BY-SA, no sentence from any source.
- No runtime case mapping, transliteration or locale lookup: what a value needs is in the data.
- Work is tracked in Jira project TAIHEI; commits are `TAIHEI-12: subject` with a body that explains the
  change to a reader without access to the ticket.
