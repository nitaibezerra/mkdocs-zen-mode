"""MkDocs Zen Mode plugin — injects zen mode toggle into rendered pages."""

from pathlib import Path

from mkdocs.config import config_options
from mkdocs.config.base import Config
from mkdocs.plugins import BasePlugin, get_plugin_logger

log = get_plugin_logger(__name__)

ASSETS_DIR = Path(__file__).parent / "assets"

# SVG icons: fullscreen (expand) and fullscreen_exit (collapse)
# Material Design icons from https://fonts.google.com/icons
ICON_EXPAND = (
    '<svg class="zen-icon-expand" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 '
    '7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>'
    "</svg>"
)
ICON_COLLAPSE = (
    '<svg class="zen-icon-collapse" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
    '<path d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 '
    '11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"/>'
    "</svg>"
)


class ZenModeConfig(Config):
    enabled = config_options.Type(bool, default=True)
    max_width = config_options.Type(str, default="780px")
    shortcut = config_options.Type(str, default="Alt+Z")
    storage_key = config_options.Type(str, default="mkdocs-zen-mode")
    button_position = config_options.Choice(("header", "none"), default="header")
    hide_header = config_options.Type(bool, default=True)
    hide_footer = config_options.Type(bool, default=True)
    hide_tabs = config_options.Type(bool, default=True)
    hide_toc = config_options.Type(bool, default=True)
    hide_nav = config_options.Type(bool, default=True)
    transition_duration = config_options.Type(str, default="0.3s")


class ZenModePlugin(BasePlugin[ZenModeConfig]):
    def on_config(self, config, **kwargs):
        if not self.config.enabled:
            return config
        self._css = self._load_asset("zen-mode.css")
        self._js = self._load_asset("zen-mode.js")
        return config

    def on_post_page(self, output, page, config, **kwargs):
        if not self.config.enabled:
            return output

        css = self._render_css()
        js = self._render_js()
        button_html = self._build_button_html()

        # Inject <style> before </head>
        output = output.replace("</head>", f"<style>{css}</style>\n</head>", 1)

        # Inject button into header
        if self.config.button_position == "header":
            output = self._inject_button(output, button_html)

        # Inject <script> before </body>
        output = output.replace("</body>", f"<script>{js}</script>\n</body>", 1)

        return output

    # --- Private helpers ---

    def _load_asset(self, filename):
        return (ASSETS_DIR / filename).read_text(encoding="utf-8")

    def _render_css(self):
        css = self._css
        css = css.replace("{{MAX_WIDTH}}", self.config.max_width)
        css = css.replace("{{TRANSITION}}", self.config.transition_duration)

        # Remove CSS rules for elements the user doesn't want to hide
        hide_map = {
            "hide_nav": "body.zen-mode-active .md-sidebar--primary",
            "hide_toc": "body.zen-mode-active .md-sidebar--secondary",
            "hide_header": "body.zen-mode-active .md-header",
            "hide_footer": "body.zen-mode-active .md-footer",
            "hide_tabs": "body.zen-mode-active .md-tabs",
        }
        for config_key, selector in hide_map.items():
            if not getattr(self.config, config_key):
                css = self._remove_css_block(css, selector)

        return css

    def _render_js(self):
        js = self._js
        js = js.replace("{{STORAGE_KEY}}", self.config.storage_key)
        js = js.replace("{{SHORTCUT}}", self.config.shortcut)
        return js

    @staticmethod
    def _remove_css_block(css, selector):
        """Remove a CSS rule block by its selector (simple single-level braces)."""
        start = css.find(selector)
        if start == -1:
            return css
        brace_open = css.find("{", start)
        if brace_open == -1:
            return css
        brace_close = css.find("}", brace_open)
        if brace_close == -1:
            return css
        return css[:start] + css[brace_close + 1 :]

    def _build_button_html(self):
        return (
            '<button class="md-header__button md-icon zen-mode-toggle" '
            f'title="Toggle Zen Mode ({self.config.shortcut})" '
            'aria-label="Toggle Zen Mode" aria-pressed="false">'
            f"{ICON_EXPAND}{ICON_COLLAPSE}"
            "</button>"
        )

    @staticmethod
    def _inject_button(output, button_html):
        # Insert before the search component in the header.
        # Material 9.x uses <div class="md-search">, older versions use <form class="md-search".
        markers = [
            '<div class="md-search"',
            '<form class="md-search"',
            '<div class="md-header__source"',
        ]
        for marker in markers:
            if marker in output:
                return output.replace(marker, button_html + marker, 1)
        # Fallback: before closing </nav> in header
        if "</nav>" in output:
            return output.replace("</nav>", button_html + "</nav>", 1)
        log.warning("zen-mode: could not find header marker to inject button")
        return output
