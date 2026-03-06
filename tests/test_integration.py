"""Integration tests — full MkDocs build with zen-mode plugin."""

import shutil
import tempfile
from pathlib import Path

import pytest
from mkdocs.commands import build
from mkdocs.config import load_config


@pytest.fixture(scope="module")
def build_site():
    """Build a minimal MkDocs Material site with zen-mode enabled (once per module)."""
    tmpdir = tempfile.mkdtemp()
    docs_dir = Path(tmpdir) / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Hello\n\nTest page for zen mode.\n")
    (docs_dir / "second.md").write_text("# Second Page\n\nAnother page.\n")

    mkdocs_yml = Path(tmpdir) / "mkdocs.yml"
    mkdocs_yml.write_text(
        "site_name: Zen Mode Test\n"
        "theme:\n"
        "  name: material\n"
        "plugins:\n"
        "  - search\n"
        "  - zen-mode:\n"
        "      max_width: '800px'\n"
        "      shortcut: 'Alt+Z'\n"
    )

    cfg = load_config(str(mkdocs_yml))
    build.build(cfg)

    site_dir = Path(tmpdir) / "site"
    yield site_dir

    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope="module")
def build_site_partial_hide():
    """Build with some hide options disabled."""
    tmpdir = tempfile.mkdtemp()
    docs_dir = Path(tmpdir) / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Hello\n\nPartial hide test.\n")

    mkdocs_yml = Path(tmpdir) / "mkdocs.yml"
    mkdocs_yml.write_text(
        "site_name: Partial Hide Test\n"
        "theme:\n"
        "  name: material\n"
        "plugins:\n"
        "  - search\n"
        "  - zen-mode:\n"
        "      hide_toc: false\n"
        "      hide_header: false\n"
    )

    cfg = load_config(str(mkdocs_yml))
    build.build(cfg)

    site_dir = Path(tmpdir) / "site"
    yield site_dir

    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture(scope="module")
def build_site_disabled():
    """Build with zen-mode disabled."""
    tmpdir = tempfile.mkdtemp()
    docs_dir = Path(tmpdir) / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Hello\n\nDisabled test.\n")

    mkdocs_yml = Path(tmpdir) / "mkdocs.yml"
    mkdocs_yml.write_text(
        "site_name: Disabled Test\n"
        "theme:\n"
        "  name: material\n"
        "plugins:\n"
        "  - search\n"
        "  - zen-mode:\n"
        "      enabled: false\n"
    )

    cfg = load_config(str(mkdocs_yml))
    build.build(cfg)

    site_dir = Path(tmpdir) / "site"
    yield site_dir

    shutil.rmtree(tmpdir, ignore_errors=True)


class TestFullBuild:
    def test_index_has_zen_style(self, build_site):
        index = (build_site / "index.html").read_text()
        assert "<style>" in index
        assert "zen-mode-active" in index

    def test_index_has_zen_script(self, build_site):
        index = (build_site / "index.html").read_text()
        assert "<script>" in index
        assert "mkdocs-zen-mode" in index

    def test_index_has_toggle_button(self, build_site):
        index = (build_site / "index.html").read_text()
        assert "zen-mode-toggle" in index

    def test_custom_max_width(self, build_site):
        index = (build_site / "index.html").read_text()
        assert "800px" in index

    def test_second_page_also_injected(self, build_site):
        second = (build_site / "second" / "index.html").read_text()
        assert "zen-mode-toggle" in second
        assert "zen-mode-active" in second

    def test_no_placeholder_remnants(self, build_site):
        index = (build_site / "index.html").read_text()
        assert "{{MAX_WIDTH}}" not in index
        assert "{{TRANSITION}}" not in index
        assert "{{STORAGE_KEY}}" not in index
        assert "{{SHORTCUT}}" not in index

    def test_has_aria_attributes(self, build_site):
        index = (build_site / "index.html").read_text()
        assert 'aria-label="Toggle Zen Mode"' in index
        assert 'aria-pressed="false"' in index

    def test_has_fab_styles(self, build_site):
        index = (build_site / "index.html").read_text()
        assert "zen-mode-fab" in index


class TestPartialHideBuild:
    def test_toc_css_removed_when_hide_toc_false(self, build_site_partial_hide):
        index = (build_site_partial_hide / "index.html").read_text()
        assert "body.zen-mode-active .md-sidebar--secondary" not in index

    def test_header_css_removed_when_hide_header_false(self, build_site_partial_hide):
        index = (build_site_partial_hide / "index.html").read_text()
        assert "body.zen-mode-active .md-header" not in index

    def test_nav_css_still_present(self, build_site_partial_hide):
        index = (build_site_partial_hide / "index.html").read_text()
        assert "body.zen-mode-active .md-sidebar--primary" in index

    def test_footer_css_still_present(self, build_site_partial_hide):
        index = (build_site_partial_hide / "index.html").read_text()
        assert "body.zen-mode-active .md-footer" in index


class TestDisabledBuild:
    def test_no_zen_mode_injected(self, build_site_disabled):
        index = (build_site_disabled / "index.html").read_text()
        assert "zen-mode-toggle" not in index
        assert "zen-mode-active" not in index
