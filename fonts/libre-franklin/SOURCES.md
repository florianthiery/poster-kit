# Libre Franklin (static instances)

Licence: SIL Open Font License 1.1 (`OFL.txt`). Copyright 2020 The Libre Franklin Project Authors (https://github.com/googlefonts/Libre-Franklin).

Google Fonts ships Libre Franklin only as variable fonts (`LibreFranklin[wght].ttf` and `LibreFranklin-Italic[wght].ttf`, weight axis 100 to 900). reportlab cannot select a weight on a variable font, so the four static instances below were cut once with `fontTools.varLib.instancer` at weights 400 and 700 by `tools/make_static_librefranklin.py`. They are derived (modified) fonts under the same licence; the Reserved Font Name clause does not apply, as none is declared.

Variable sources: https://raw.githubusercontent.com/google/fonts/main/ofl/librefranklin/ , retrieved 2026-10-09.

| File | Source | SHA-256 |
|---|---|---|
| `LibreFranklin-Regular.ttf` | instance wght=400 of the roman variable font | `e1b6daccd126231446719ed4c6c4a258f90dc165b491a8070db16a4ca60e48f0` |
| `LibreFranklin-Bold.ttf` | instance wght=700 of the roman variable font | `b95f6f9563db49e47618ce5c76d55160fbae39a6ce8c9e5ef0bcb718fbf9945a` |
| `LibreFranklin-Italic.ttf` | instance wght=400 of the italic variable font | `b363fe391ff4fd1a0bf2e697dbe62e5d6cfc21ee0029a3fa3b6629d78ded3e70` |
| `LibreFranklin-BoldItalic.ttf` | instance wght=700 of the italic variable font | `f04329c0deb30119c613bb12debe4c05bdcca2cd2f9bdae44405b693b0860350` |
