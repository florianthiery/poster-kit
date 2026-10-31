"""Orchestrator: the only entry point of this repository.

    python main.py                       all steps, in order
    python main.py --list                print steps and exit
    python main.py --only render         one step
    python main.py --from render         this step and everything after
    python main.py --skip preview        everything but this
    python main.py --dry-run             print the plan, run nothing
    python main.py --strict              warnings become errors (what the release check runs)
    python main.py --theme nfdi4objects  build with another theme than poster.yaml names
    python main.py --list-themes         print the available themes and exit
    python main.py --new-theme mylab     create themes/mylab/ from a base theme (--base, default neutral)
    python main.py --poster demo         build posters/demo/ (needed when there is more than one poster)
    python main.py --list-posters        print the posters and exit
    python main.py --new-poster chnt31   create posters/chnt31/ from posters/_template (--from-poster demo to copy another)
    python main.py --poster demo --blocks   print the block table (id, role, why) as Markdown for the poster's PRIMER.md

Each step is a module in py/ that also runs standalone, for example
``python py/step_render.py``. Steps run as child processes, so --list and
--dry-run import nothing heavy.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = ROOT / "py"
THEMES = ROOT / "themes"

STEPS = [
    ("validate", "step_validate.py", "check poster.yaml, the theme (incl. contrast) and the files they point to"),
    ("render", "step_render.py", "draw dist/poster.pdf and dist/layout_report.txt"),
    ("preview", "step_preview.py", "rasterise dist/poster-preview.png"),
]
NAMES = [s[0] for s in STEPS]


def select(args: argparse.Namespace) -> list[tuple[str, str, str]]:
    for opt in (args.only, args.from_step, *(args.skip or [])):
        if opt and opt not in NAMES:
            raise SystemExit(f"unknown step '{opt}'; choose from: {', '.join(NAMES)}")
    chosen = list(STEPS)
    if args.only:
        chosen = [s for s in chosen if s[0] == args.only]
    if args.from_step:
        chosen = chosen[NAMES.index(args.from_step):]
    if args.skip:
        chosen = [s for s in chosen if s[0] not in args.skip]
    return chosen


def list_themes() -> int:
    sys.path.insert(0, str(PY))
    import yaml

    ids = sorted(p.name for p in THEMES.iterdir() if p.is_dir() and (p / "theme.yaml").is_file() and not p.name.startswith("_"))
    for tid in ids:
        data = yaml.safe_load((THEMES / tid / "theme.yaml").read_text(encoding="utf-8")) or {}
        src = (data.get("source") or {}).get("name", "")
        fam = (data.get("typography") or {}).get("family", "")
        vs = ", ".join(f"{k} ({(x or {}).get('label', '')})" for k, x in (data.get("variants") or {}).items())
        print(f"{tid:18s} {data.get('state', 'ready'):8s} {data.get('name', ''):30s} {fam:22s} {src}")
        if vs:
            print(f"{'':18s} variants: {vs}   (use --theme {tid}:<variant>)")
    return 0


def new_theme(tid: str, base: str) -> int:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", tid):
        raise SystemExit("theme id: lower-case letters, digits and hyphens only")
    src, dst = THEMES / base, THEMES / tid
    if not (src / "theme.yaml").is_file():
        raise SystemExit(f"base theme '{base}' not found in themes/")
    if dst.exists():
        raise SystemExit(f"themes/{tid} already exists")
    shutil.copytree(src, dst)
    path = dst / "theme.yaml"
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^id:.*$", f"id: {tid}", text, count=1)
    text = re.sub(r"(?m)^name:.*$", f"name: \"{tid} (copy of {base}, edit me)\"", text, count=1)
    text = re.sub(r"(?m)^state:.*$", "state: pending            # set to ready once the palette is final", text, count=1)
    path.write_text(text, encoding="utf-8")
    print(f"created themes/{tid}/theme.yaml from '{base}'.")
    print("next: edit palette, tokens and typography.fonts, then run:")
    print(f"  python main.py --theme {tid}")
    return 0


def poster_ids() -> list[str]:
    root = ROOT / "posters"
    return sorted(p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("_") and (p / "poster.yaml").is_file()) if root.is_dir() else []


def list_posters() -> int:
    sys.path.insert(0, str(PY))
    import yaml

    ids = poster_ids()
    for pid in ids:
        data = yaml.safe_load((ROOT / "posters" / pid / "poster.yaml").read_text(encoding="utf-8")) or {}
        has_primer = "PRIMER.md" if (ROOT / "posters" / pid / "PRIMER.md").is_file() else "(no PRIMER.md)"
        title = (data.get("meta") or {}).get("short_title", "")
        print(f"{pid:22s} {str(data.get('theme', '')):18s} {data.get('meta', {}).get('status', ''):7s} {has_primer:15s} {title}")
    if not ids:
        print("no posters yet: python main.py --new-poster <id>")
    return 0


def new_poster(pid: str, source: str, theme: str | None) -> int:
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", pid):
        raise SystemExit("poster id: lower-case letters, digits and hyphens only")
    src, dst = ROOT / "posters" / source, ROOT / "posters" / pid
    if not (src / "poster.yaml").is_file():
        raise SystemExit(f"poster '{source}' not found in posters/")
    if dst.exists():
        raise SystemExit(f"posters/{pid} already exists")
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("dist", "__pycache__"))
    for name in ("PRIMER.md", "poster.yaml", "brief.yaml"):
        f = dst / name
        if f.is_file():
            f.write_text(f.read_text(encoding="utf-8").replace("{{id}}", pid), encoding="utf-8")
    if theme:
        f = dst / "poster.yaml"
        text = f.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^theme:\s*\S+", f"theme: {theme}", text, count=1)
        f.write_text(text, encoding="utf-8")
    if not (dst / "PRIMER.md").is_file():
        (dst / "PRIMER.md").write_text((ROOT / "posters" / "_template" / "PRIMER.md").read_text(encoding="utf-8").replace("{{id}}", pid), encoding="utf-8")
    print(f"created posters/{pid}/ from '{source}'.")
    print("next: open posters/%s/PRIMER.md (Teil A1: Anlass), edit poster.yaml and content/, then run:" % pid)
    print(f"  python main.py --poster {pid}")
    return 0


def print_blocks(pid: str | None) -> int:
    sys.path.insert(0, str(PY))
    import poster_utils as U
    import yaml

    U.select_poster(pid)
    cfg = yaml.safe_load(U.CONFIG.read_text(encoding="utf-8"))
    print("| Block | Rolle | Titel | Warum | Quelle / Stand |")
    print("|---|---|---|---|---|")
    order = [b for band in cfg["layout"]["bands"] for col in band["columns"] for b in col["blocks"]]
    for bid in order:
        b = cfg["blocks"][bid]
        cell = lambda s: str(s or "").replace("|", "/").replace("\n", " ")
        print(f"| `{bid}` | {cell(b.get('role') or b.get('accent'))} | {cell(b.get('title'))} | {cell(b.get('why'))} | |")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the poster PDF.")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--from", dest="from_step")
    ap.add_argument("--skip", action="append")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--theme", help="theme id, overrides 'theme:' in poster.yaml")
    ap.add_argument("--list-themes", action="store_true")
    ap.add_argument("--new-theme", metavar="ID")
    ap.add_argument("--base", default="neutral", help="base theme for --new-theme")
    ap.add_argument("--poster", help="poster id: the folder in posters/ to build")
    ap.add_argument("--list-posters", action="store_true")
    ap.add_argument("--new-poster", metavar="ID")
    ap.add_argument("--from-poster", default="_template", help="poster to copy for --new-poster (default: _template)")
    ap.add_argument("--blocks", action="store_true", help="print the block table for the poster's PRIMER.md")
    args = ap.parse_args()

    if args.list:
        for name, script, text in STEPS:
            print(f"{name:10s} py/{script:20s} {text}")
        return 0
    if args.list_themes:
        return list_themes()
    if args.list_posters:
        return list_posters()
    if args.new_poster:
        return new_poster(args.new_poster, args.from_poster, args.theme)
    if args.blocks:
        return print_blocks(args.poster)
    if args.new_theme:
        return new_theme(args.new_theme, args.base)
    chosen = select(args)
    sys.path.insert(0, str(PY))
    import poster_utils as U

    pid = U.select_poster(args.poster)          # fails early with the list of posters if it is ambiguous
    extra = (["--strict"] if args.strict else []) + (["--theme", args.theme] if args.theme else []) + ["--poster", pid]
    if args.dry_run:
        for name, script, _ in chosen:
            print(f"would run: {name} (py/{script})" + (" " + " ".join(extra) if extra else ""))
        return 0

    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    log: list[str] = []
    timings: list[tuple[str, float]] = []
    failed = False

    def say(line: str) -> None:
        print(line)
        log.append(line)

    for name, script, _ in chosen:
        say(f"== {name}")
        cmd = [sys.executable, str(PY / script)] + extra
        t0 = time.perf_counter()
        proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
        timings.append((name, time.perf_counter() - t0))
        for line in (proc.stdout + proc.stderr).splitlines():
            say("   " + line)
        if proc.returncode != 0:
            say(f"!! step '{name}' failed (exit {proc.returncode})")
            failed = True
            break

    total = sum(t for _, t in timings) or 1.0
    say("== timing")
    for name, t in timings:
        say(f"   {name:10s} {t:6.2f} s  {100 * t / total:4.0f} %")
    say(f"== poster: {pid}")
    say("== result: FAILED" if failed else "== result: ok")
    REPORT = U.DIST / "pipeline_report.txt"
    REPORT.parent.mkdir(exist_ok=True)
    # The report carries no timings so that two identical runs give identical bytes.
    stable = [l for l in log if not (l.startswith("   ") and l.rstrip().endswith("%") and " s " in l)]
    stable = [l for l in stable if l != "== timing"]
    REPORT.write_text("\n".join(stable) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
