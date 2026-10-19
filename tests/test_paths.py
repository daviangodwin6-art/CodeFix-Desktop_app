"""agent/paths.py: from source nothing moves; frozen (desktop build), writes go to %APPDATA%\\CodeFix."""
import importlib
import sys

import pytest

from agent import paths, runner


@pytest.fixture
def frozen(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path / "bundle"), raising=False)
    monkeypatch.setenv("APPDATA", str(tmp_path / "appdata"))
    yield importlib.reload(paths)
    monkeypatch.undo()
    importlib.reload(paths)


def test_from_source_everything_stays_in_the_repo(monkeypatch):
    monkeypatch.delenv("CODEFIX_HOME")
    assert not paths.FROZEN
    assert paths.bundle_dir() == paths.data_dir() == paths.home() == paths.SOURCE_ROOT
    assert (paths.bundle_dir() / "frontend" / "dist" / "index.html").is_file()
    assert runner.base_python() == sys.executable


def test_frozen_reads_the_bundle_and_writes_to_appdata(frozen, tmp_path, monkeypatch):
    assert frozen.bundle_dir() == tmp_path / "bundle"
    assert frozen.env_file() == tmp_path / "appdata" / "CodeFix" / ".env"
    monkeypatch.delenv("CODEFIX_HOME")
    assert frozen.home() == tmp_path / "appdata" / "CodeFix"
    monkeypatch.setenv("CODEFIX_HOME", str(tmp_path / "elsewhere"))
    assert frozen.home() == tmp_path / "elsewhere"
