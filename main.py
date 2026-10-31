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
REPORT = ROOT / "dist" / "pipeline_report.txt"

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
        print(f"{tid:18s} {data.get('state', 'ready'):8s} {data.get('name', ''):30s} {fam:22s} {src}")
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
    args = ap.parse_args()

    if args.list:
        for name, script, text in STEPS:
            print(f"{name:10s} py/{script:20s} {text}")
        return 0
    if args.list_themes:
        return list_themes()
    if args.new_theme:
        return new_theme(args.new_theme, args.base)
    chosen = select(args)
    extra = (["--strict"] if args.strict else []) + (["--theme", args.theme] if args.theme else [])
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
    say("== result: FAILED" if failed else "== result: ok")
    REPORT.parent.mkdir(exist_ok=True)
    # The report carries no timings so that two identical runs give identical bytes.
    stable = [l for l in log if not (l.startswith("   ") and l.rstrip().endswith("%") and " s " in l)]
    stable = [l for l in stable if l != "== timing"]
    REPORT.write_text("\n".join(stable) + "\n", encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
