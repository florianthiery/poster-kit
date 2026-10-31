"""Build every poster (and, on request, every poster in every theme) in one go.

    python tools/build_all.py                  every poster with its own theme -> posters/<id>/dist/
    python tools/build_all.py --all-themes     additionally one PDF and PNG per theme -> posters/<id>/dist/themes/
    python tools/build_all.py --poster demo    only this poster
    python tools/build_all.py --strict         release check for the posters whose meta.status is final
    python tools/build_all.py --check-repro    build each poster twice and compare the bytes of poster.pdf

Each build is a normal ``python main.py`` run, so everything it prints and checks applies. The last build of
each poster is always the one with its own theme, so dist/poster.pdf is never left in a borrowed look.
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "py"))
import poster_utils as U  # noqa: E402
import theme as T  # noqa: E402


def run(args: list[str]) -> int:
    proc = subprocess.run([sys.executable, str(ROOT / "main.py")] + args, cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8")
    for line in (proc.stdout + proc.stderr).splitlines():
        if line.startswith("   ") and ("WARNING" in line or "ERROR" in line or "wrote" in line):
            print(line)
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--poster")
    ap.add_argument("--all-themes", action="store_true")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--check-repro", action="store_true")
    args = ap.parse_args()
    posters = [args.poster] if args.poster else U.list_posters()
    if args.strict and not args.poster:
        # a poster that is still a draft is expected to have open points; only 'final' claims to be ready
        import yaml
        final = []
        for pid in posters:
            meta = (yaml.safe_load((U.POSTERS / pid / "poster.yaml").read_text(encoding="utf-8")) or {}).get("meta", {})
            (final if meta.get("status") == "final" else []).append(pid)
        skipped = [p for p in posters if p not in final]
        if skipped:
            print(f"== strict check skipped for posters not marked final: {', '.join(skipped)}")
        posters = final
    if not posters:
        print("no posters to build" + (" (none is marked final)" if args.strict else " in posters/"))
        return 0 if args.strict else 1
    strict = ["--strict"] if args.strict else []
    failed = []
    for pid in posters:
        print(f"== {pid}")
        U.select_poster(pid)
        dist = U.DIST
        if args.all_themes:
            out = dist / "themes"
            out.mkdir(parents=True, exist_ok=True)
            for tid in T.all_specs():
                code = run(["--poster", pid, "--theme", tid])
                if code == 0:
                    shutil.copyfile(dist / "poster.pdf", out / f"poster-{tid.replace(':', '-')}.pdf")
                    shutil.copyfile(dist / "poster-preview.png", out / f"poster-{tid.replace(':', '-')}.png")
                    print(f"   {tid}: ok")
                else:
                    print(f"   {tid}: FAILED")
                    failed.append(f"{pid}/{tid}")
        code = run(["--poster", pid] + strict)
        print(f"   {pid}: {'ok' if code == 0 else 'FAILED'}")
        if code != 0:
            failed.append(pid)
        elif args.check_repro:
            first = hashlib.sha256((dist / "poster.pdf").read_bytes()).hexdigest()
            run(["--poster", pid] + strict)
            second = hashlib.sha256((dist / "poster.pdf").read_bytes()).hexdigest()
            print(f"   {pid}: rebuild {'identical' if first == second else 'DIFFERENT'} ({first[:12]})")
            if first != second:
                failed.append(f"{pid} (not reproducible)")
    print("== done" + (": FAILED " + ", ".join(failed) if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
