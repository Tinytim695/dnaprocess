import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "dnaprocess"


def run(*args):
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_snapshot_current_process(tmp_path):
    result = run("snapshot", str(os.getpid()), "-o", str(tmp_path / "one.json"))
    assert result.returncode == 0

    data = json.loads((tmp_path / "one.json").read_text(encoding="utf-8"))
    assert data["schema"] == 1
    assert data["process"]["pid"] == os.getpid()
    assert len(data["process"]["fingerprint_sha256"]) == 64
    assert "environment" not in data["process"]


def test_diff_identical_snapshot(tmp_path):
    first = tmp_path / "before.json"
    second = tmp_path / "after.json"
    assert run("snapshot", str(os.getpid()), "-o", str(first)).returncode == 0
    assert run("snapshot", str(os.getpid()), "-o", str(second)).returncode == 0

    result = run("diff", str(first), str(second))
    assert result.returncode == 0
    assert "Fingerprint:" in result.stdout


def test_missing_pid(tmp_path):
    result = run("snapshot", "999999999", "-o", str(tmp_path / "x.json"))
    assert result.returncode == 1
    assert "does not exist" in result.stderr


def test_diff_detects_change(tmp_path):
    before = {
        "process": {"pid": 7, "threads": 1, "cmdline": "demo", "fingerprint_sha256": "a"}
    }
    after = {
        "process": {"pid": 7, "threads": 2, "cmdline": "demo", "fingerprint_sha256": "b"}
    }
    b = tmp_path / "b.json"
    a = tmp_path / "a.json"
    b.write_text(json.dumps(before))
    a.write_text(json.dumps(after))

    result = run("diff", str(b), str(a))
    assert result.returncode == 0
    assert "~ threads: 1 -> 2" in result.stdout
