# flake8: noqa
import pickle
import subprocess
from pathlib import Path

import httpx
import pytest
from platformdirs.api import PlatformDirsABC
from pytest_mock import MockerFixture


from oembedpy import application


@pytest.fixture
def mocked_workspace(monkeypatch, tmp_path):
    def _append_app_name_and_version(*arg, **kwargs):
        return tmp_path

    monkeypatch.setattr(
        PlatformDirsABC,
        "_append_app_name_and_version",
        _append_app_name_and_version,
    )
    ws = application.Workspace()
    return ws


@pytest.mark.skipif("sys.platform != 'linux'")
def test_workspace():
    ws = application.Workspace()
    assert ws.cache_dir == Path.home() / ".local" / "share/oembedpy"


@pytest.mark.skipif("sys.platform != 'linux'")
class TestForWorkspace:
    def test_properties(self, mocked_workspace: application.Workspace, tmp_path):
        assert mocked_workspace.cache_dir == tmp_path

    def test_cache_providers_json(
        self, mocked_workspace: application.Workspace, tmp_path
    ):
        mocked_workspace.init()
        assert (tmp_path / "providers.json").exists()
        assert mocked_workspace._registry is not None

    def test_fetch_using_cached_providers_json(
        self, mocked_workspace: application.Workspace, mocker: MockerFixture, tmp_path
    ):
        spy = mocker.spy(httpx, "get")
        mocked_workspace.init()
        assert spy.call_count == 1
        other_workspace = application.Workspace()
        other_workspace.init()
        assert spy.call_count == 1

    def test_purge_cached_providers_json(
        self, mocked_workspace: application.Workspace, mocker: MockerFixture, tmp_path
    ):
        spy = mocker.spy(httpx, "get")
        mocked_workspace.init()
        assert spy.call_count == 1
        subprocess.run(
            [
                "touch",
                "-t",
                "200001010000",
                (mocked_workspace.cache_dir / "providers.json"),
            ]
        )
        other_workspace = application.Workspace()
        other_workspace.init()
        assert spy.call_count == 2

    def test_initialized_response_cache(
        self, mocked_workspace: application.Workspace, tmp_path
    ):
        mocked_workspace.init()
        assert (tmp_path / "providers.json").exists()
        mocked_workspace.__del__()
        assert (tmp_path / "db.pickle").exists()

    def test_initialized_response_cache(
        self, mocked_workspace: application.Workspace, tmp_path
    ):
        mocked_workspace.init()
        mocked_workspace.fetch(
            "https://bsky.app/profile/attakei.dev/post/3kr76heazfp2i"
        )
        mocked_workspace.__del__()
        db_path = tmp_path / "db.pickle"
        assert db_path.exists()
        db = pickle.loads(db_path.read_bytes())
        assert len(db) == 1
