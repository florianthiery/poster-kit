# Font library

Shared by all themes. A theme refers to files here by repository-relative path in `themes/<id>/theme.yaml`, section `typography`.

| Folder | Families | Licence | Used by |
|---|---|---|---|
| `dejavu/` | DejaVu Sans Condensed, DejaVu Sans Bold, DejaVu Sans Mono | Bitstream Vera / DejaVu | `neutral` (and the mono fallback) |
| `fira-sans/` | Fira Sans, Fira Mono | SIL OFL 1.1 | `chublets`, `research-squirrel` |
| `pt-sans/` | PT Sans, PT Mono | SIL OFL 1.1 | `nfdi4objects` |
| `libre-franklin/` | Libre Franklin (static instances) | SIL OFL 1.1 | `leiza` |
| `barlow/` | Barlow, Barlow Semi Condensed Bold | SIL OFL 1.1 | `caa-uk` |

Each folder has a `SOURCES.md` with origin, retrieval date and SHA-256 of every file. The licence texts stay next to the fonts and must travel with them.

A fork that uses only one theme can delete the other folders to save space; keep the folder of the theme in use and `dejavu/` if any theme uses `DejaVuSansMono.ttf` as its monospace face.
