"""Verify that artifacts/versions/<vN>/ match the hashes recorded in the team's runs.

Run from starter_v0/:  python scripts/verify_versions.py
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from versioning import file_hash  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VERSIONS_DIR = ROOT / "artifacts" / "versions"


def expected_hashes() -> dict[str, tuple[str, str]]:
    out: dict[str, tuple[str, str]] = {}
    for run_file in sorted(glob.glob(str(ROOT / "runs" / "v*_B_base_*.json"))):
        run = json.loads(Path(run_file).read_text(encoding="utf-8"))
        out.setdefault(run["version"], (run["prompt_hash"], run["tools_hash"]))
    return out


def main() -> int:
    ok = True
    expected = expected_hashes()
    current = ("artifacts/system_prompt.md", "artifacts/tools.yaml")
    for version, (want_prompt, want_tools) in sorted(expected.items()):
        folder = VERSIONS_DIR / version
        prompt = folder / "system_prompt.md"
        tools = folder / "tools.yaml"
        if prompt.exists() and tools.exists():
            label = f"{version} (artifacts/versions/{version})"
        elif version == max(expected):
            # latest version lives in artifacts/ itself
            prompt, tools = ROOT / current[0], ROOT / current[1]
            label = f"{version} (artifacts/ current)"
        else:
            ok = False
            print(f"[MISSING] {version}: put system_prompt.md + tools.yaml in {folder.relative_to(ROOT)}/ "
                  f"(expected prompt {want_prompt[:12]}, tools {want_tools[:12]})")
            continue
        got_prompt, got_tools = file_hash(prompt), file_hash(tools)
        match = got_prompt == want_prompt and got_tools == want_tools
        ok &= match
        print(f"[{'OK' if match else 'MISMATCH'}] {label}: prompt {got_prompt[:12]} vs {want_prompt[:12]} | tools {got_tools[:12]} vs {want_tools[:12]}")
    print("RESULT:", "ALL MATCH" if ok else "SOME MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
