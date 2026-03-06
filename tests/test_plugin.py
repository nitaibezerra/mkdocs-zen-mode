"""Unit tests for ZenModePlugin."""

from mkdocs_zen_mode.plugin import ZenModePlugin

from .conftest import SAMPLE_MATERIAL_HTML


# ---------------------------------------------------------------------------
# Helper to create a plugin with custom config in one line
# ---------------------------------------------------------------------------
def _make_plugin(**overrides):
    p = ZenModePlugin()
    p.load_config(overrides)
    p.on_config({})
    return p


# ===========================================================================
# Config defaults and validation
# ===========================================================================
class TestConfig:
    def test_all_defaults(self, plugin):
        c = plugin.config
        assert c.enabled is True
        assert c.max_width == "780px"
        assert c.shortcut == "Alt+Z"
        assert c.storage_key == "mkdocs-zen-mode"
        assert c.button_position == "header"
        assert c.hide_header is True
        assert c.hide_footer is True
        assert c.hide_tabs is True
        assert c.hide_toc is True
        assert c.hide_nav is True
        assert c.hide_announce is True
        assert c.transition_duration == "0.3s"

    def test_custom_values_applied(self):
        p = _make_plugin(max_width="900px", shortcut="Ctrl+Shift+Z", storage_key="my-key")
        assert p.config.max_width == "900px"
        assert p.config.shortcut == "Ctrl+Shift+Z"
        assert p.config.storage_key == "my-key"

    def test_invalid_button_position_raises(self):
        p = ZenModePlugin()
        errors, warnings = p.load_config({"button_position": "invalid"})
        assert errors  # should have validation errors

    def test_disabled_skips_asset_loading(self, disabled_plugin):
        assert not hasattr(disabled_plugin, "_css")
        assert not hasattr(disabled_plugin, "_js")


# ===========================================================================
# HTML injection positions
# ===========================================================================
class TestHtmlInjection:
    def test_style_injected_before_head_close(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "<style>" in result
        assert result.index("<style>") < result.index("</head>")

    def test_script_injected_before_body_close(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "<script>" in result
        assert result.index("<script>") < result.index("</body>")

    def test_button_injected_before_search_material9(self, plugin, sample_html):
        """Material 9.x: button should appear before <div class='md-search'>."""
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "zen-mode-toggle" in result
        toggle_pos = result.index("zen-mode-toggle")
        search_pos = result.index('class="md-search"')
        assert toggle_pos < search_pos

    def test_button_injected_before_search_legacy(self, plugin, sample_html_legacy):
        """Older Material: button should appear before <form class='md-search'>."""
        result = plugin.on_post_page(sample_html_legacy, page=None, config={})
        assert "zen-mode-toggle" in result
        toggle_pos = result.index("zen-mode-toggle")
        search_pos = result.index('class="md-search"')
        assert toggle_pos < search_pos

    def test_button_not_injected_when_position_none(self):
        p = _make_plugin(button_position="none")
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert '<button class="md-header__button md-icon zen-mode-toggle"' not in result
        # CSS and JS should still be injected
        assert "<style>" in result
        assert "<script>" in result

    def test_disabled_returns_unmodified(self, disabled_plugin, sample_html):
        result = disabled_plugin.on_post_page(sample_html, page=None, config={})
        assert result == sample_html

    def test_injection_is_idempotent_concepts(self, plugin, sample_html):
        """Single injection per page — no duplicates."""
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert result.count("<style>") == 1
        assert result.count("<script>") == 1


# ===========================================================================
# Placeholder substitution
# ===========================================================================
class TestPlaceholderSubstitution:
    def test_max_width_replaced(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "780px" in result
        assert "{{MAX_WIDTH}}" not in result

    def test_transition_replaced(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "0.3s" in result
        assert "{{TRANSITION}}" not in result

    def test_storage_key_replaced(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert '"mkdocs-zen-mode"' in result
        assert "{{STORAGE_KEY}}" not in result

    def test_shortcut_replaced(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "Alt+Z" in result
        assert "{{SHORTCUT}}" not in result

    def test_no_placeholders_remain(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "{{" not in result
        assert "}}" not in result

    def test_custom_max_width(self):
        p = _make_plugin(max_width="1000px")
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "1000px" in result
        assert "780px" not in result

    def test_custom_shortcut(self):
        p = _make_plugin(shortcut="Ctrl+Shift+F")
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "Ctrl+Shift+F" in result

    def test_custom_storage_key(self):
        p = _make_plugin(storage_key="my-custom-zen")
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "my-custom-zen" in result

    def test_custom_transition_duration(self):
        p = _make_plugin(transition_duration="0.5s")
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "0.5s" in result


# ===========================================================================
# hide_* configuration options
# ===========================================================================
class TestHideOptions:
    def test_hide_header_false_removes_header_css(self):
        p = _make_plugin(hide_header=False)
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "body.zen-mode-active .md-header" not in result

    def test_hide_footer_false_removes_footer_css(self):
        p = _make_plugin(hide_footer=False)
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "body.zen-mode-active .md-footer" not in result

    def test_hide_tabs_false_removes_tabs_css(self):
        p = _make_plugin(hide_tabs=False)
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "body.zen-mode-active .md-tabs" not in result

    def test_hide_nav_false_removes_primary_sidebar_css(self):
        p = _make_plugin(hide_nav=False)
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "body.zen-mode-active .md-sidebar--primary" not in result
        # TOC should still be hidden
        assert "body.zen-mode-active .md-sidebar--secondary" in result

    def test_hide_toc_false_removes_secondary_sidebar_css(self):
        p = _make_plugin(hide_toc=False)
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "body.zen-mode-active .md-sidebar--secondary" not in result
        # Nav should still be hidden
        assert "body.zen-mode-active .md-sidebar--primary" in result

    def test_hide_announce_false_removes_banner_css(self):
        p = _make_plugin(hide_announce=False)
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "body.zen-mode-active .md-banner" not in result

    def test_hide_announce_true_keeps_banner_css(self):
        p = _make_plugin(hide_announce=True)
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert "body.zen-mode-active .md-banner" in result

    def test_all_hide_false_still_has_content_centering(self):
        p = _make_plugin(
            hide_header=False, hide_footer=False, hide_tabs=False,
            hide_nav=False, hide_toc=False, hide_announce=False,
        )
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        # Content centering should still be present
        assert "body.zen-mode-active .md-main__inner" in result
        assert "body.zen-mode-active .md-content" in result


# ===========================================================================
# Button fallback markers
# ===========================================================================
class TestButtonFallback:
    def test_material9_div_search_marker(self, plugin, sample_html):
        """Primary marker: <div class='md-search'>."""
        result = plugin.on_post_page(sample_html, page=None, config={})
        btn_pos = result.index("zen-mode-toggle")
        search_pos = result.index('class="md-search"')
        assert btn_pos < search_pos

    def test_legacy_form_search_marker(self, plugin, sample_html_legacy):
        """Fallback: <form class='md-search'>."""
        result = plugin.on_post_page(sample_html_legacy, page=None, config={})
        btn_pos = result.index("zen-mode-toggle")
        search_pos = result.index('class="md-search"')
        assert btn_pos < search_pos

    def test_fallback_to_header_source(self):
        """When no search present, falls back to header source div."""
        p = _make_plugin()
        html = '<html><head></head><body><nav><div class="md-header__source">X</div></nav></body></html>'
        result = p.on_post_page(html, page=None, config={})
        assert "zen-mode-toggle" in result
        assert result.index("zen-mode-toggle") < result.index("md-header__source")

    def test_fallback_to_nav_close(self):
        """When nothing else matches, falls back to </nav>."""
        p = _make_plugin()
        html = "<html><head></head><body><nav>Nav</nav></body></html>"
        result = p.on_post_page(html, page=None, config={})
        assert "zen-mode-toggle" in result

    def test_no_marker_at_all_still_has_css_and_js(self):
        """When no marker found, button is skipped but CSS/JS still injected."""
        p = _make_plugin()
        html = "<html><head></head><body><main>Content</main></body></html>"
        result = p.on_post_page(html, page=None, config={})
        assert '<button class="md-header__button md-icon zen-mode-toggle"' not in result
        assert "<style>" in result
        assert "<script>" in result


# ===========================================================================
# Accessibility
# ===========================================================================
class TestAccessibility:
    def test_button_has_aria_label(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert 'aria-label="Toggle Zen Mode"' in result

    def test_button_has_aria_pressed(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert 'aria-pressed="false"' in result

    def test_button_has_title_with_shortcut(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert 'title="Toggle Zen Mode (Alt+Z)"' in result

    def test_custom_shortcut_in_title(self):
        p = _make_plugin(shortcut="Ctrl+Z")
        result = p.on_post_page(SAMPLE_MATERIAL_HTML, page=None, config={})
        assert 'title="Toggle Zen Mode (Ctrl+Z)"' in result


# ===========================================================================
# CSS content validation
# ===========================================================================
class TestCssContent:
    def test_contains_zen_mode_active_body_class(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "body.zen-mode-active" in result

    def test_contains_fab_styles(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert ".zen-mode-fab" in result

    def test_contains_icon_swap_styles(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert ".zen-icon-expand" in result
        assert ".zen-icon-collapse" in result


# ===========================================================================
# JS content validation
# ===========================================================================
class TestJsContent:
    def test_contains_localstorage_logic(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "localStorage" in result

    def test_contains_keyboard_handler(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "handleKeydown" in result

    def test_contains_instant_nav_support(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "document$" in result

    def test_contains_input_guard(self, plugin, sample_html):
        """Shortcut should not fire when typing in search or text fields."""
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "INPUT" in result
        assert "TEXTAREA" in result

    def test_contains_fab_creation(self, plugin, sample_html):
        result = plugin.on_post_page(sample_html, page=None, config={})
        assert "zen-mode-fab" in result
        assert "ensureFab" in result
