"""End-to-end tests using Playwright against a live MkDocs server."""

import subprocess
import time

import pytest

playwright = pytest.importorskip("playwright.sync_api")

SERVE_PORT = 8765
SERVE_URL = f"http://127.0.0.1:{SERVE_PORT}"


@pytest.fixture(scope="module")
def server():
    """Start mkdocs serve for the example site and yield the URL."""
    proc = subprocess.Popen(
        ["mkdocs", "serve", "-a", f"127.0.0.1:{SERVE_PORT}", "--no-livereload"],
        cwd="example",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    # Wait for server to be ready
    for _ in range(30):
        time.sleep(0.5)
        try:
            import urllib.request
            urllib.request.urlopen(SERVE_URL, timeout=1)
            break
        except Exception:
            continue
    else:
        proc.kill()
        pytest.fail("MkDocs server did not start in time")

    yield SERVE_URL
    proc.terminate()
    proc.wait(timeout=5)


@pytest.fixture(scope="module")
def browser_page(server):
    """Provide a Playwright browser page connected to the server."""
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(server)
    page.wait_for_load_state("networkidle")
    yield page
    browser.close()
    pw.stop()


class TestZenModeE2E:
    def test_toggle_button_visible(self, browser_page):
        btn = browser_page.query_selector(".zen-mode-toggle")
        assert btn is not None
        assert btn.is_visible()

    def test_click_activates_zen_mode(self, browser_page):
        btn = browser_page.query_selector(".zen-mode-toggle")
        btn.click()
        browser_page.wait_for_timeout(400)

        has_class = browser_page.evaluate(
            'document.body.classList.contains("zen-mode-active")'
        )
        assert has_class is True

    def test_localstorage_persisted(self, browser_page):
        value = browser_page.evaluate('localStorage.getItem("mkdocs-zen-mode")')
        assert value == "true"

    def test_fab_visible_in_zen_mode(self, browser_page):
        fab = browser_page.query_selector(".zen-mode-fab")
        assert fab is not None
        assert fab.is_visible()

    def test_header_hidden_in_zen_mode(self, browser_page):
        header = browser_page.query_selector(".md-header")
        box = header.bounding_box()
        # Header should be translated off-screen (y < 0) or have 0 height
        assert box is None or box["y"] + box["height"] <= 0

    def test_sidebar_hidden_in_zen_mode(self, browser_page):
        sidebar = browser_page.query_selector(".md-sidebar--primary")
        if sidebar:
            box = sidebar.bounding_box()
            assert box is None or box["width"] == 0

    def test_state_persists_across_navigation(self, browser_page):
        browser_page.goto(f"{SERVE_URL}/getting-started/")
        browser_page.wait_for_load_state("networkidle")
        browser_page.wait_for_timeout(400)

        has_class = browser_page.evaluate(
            'document.body.classList.contains("zen-mode-active")'
        )
        assert has_class is True

    def test_alt_z_toggles_off(self, browser_page):
        browser_page.keyboard.press("Alt+z")
        browser_page.wait_for_timeout(400)

        has_class = browser_page.evaluate(
            'document.body.classList.contains("zen-mode-active")'
        )
        assert has_class is False

    def test_header_visible_after_toggle_off(self, browser_page):
        header = browser_page.query_selector(".md-header")
        box = header.bounding_box()
        assert box is not None
        assert box["height"] > 0

    def test_alt_z_toggles_on_again(self, browser_page):
        browser_page.keyboard.press("Alt+z")
        browser_page.wait_for_timeout(400)

        has_class = browser_page.evaluate(
            'document.body.classList.contains("zen-mode-active")'
        )
        assert has_class is True

    def test_fab_click_exits_zen_mode(self, browser_page):
        fab = browser_page.query_selector(".zen-mode-fab")
        fab.click()
        browser_page.wait_for_timeout(400)

        has_class = browser_page.evaluate(
            'document.body.classList.contains("zen-mode-active")'
        )
        assert has_class is False

    def test_shortcut_ignored_in_search_input(self, browser_page):
        """Alt+Z should not toggle zen mode when focus is in search input."""
        # Ensure zen mode is off
        browser_page.evaluate('document.body.classList.remove("zen-mode-active")')

        # Focus the search input
        search_input = browser_page.query_selector(".md-search__input")
        if search_input:
            search_input.focus()
            browser_page.keyboard.press("Alt+z")
            browser_page.wait_for_timeout(200)

            has_class = browser_page.evaluate(
                'document.body.classList.contains("zen-mode-active")'
            )
            assert has_class is False
