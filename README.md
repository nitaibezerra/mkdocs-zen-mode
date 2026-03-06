# mkdocs-zen-mode

> Zen Mode for MkDocs Material — distraction-free reading with a single click.

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-zen-mode)](https://pypi.org/project/mkdocs-zen-mode/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A plugin that adds a **Zen Mode** toggle to [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) sites. When activated, it hides the navigation sidebar, table of contents, header, footer, and tabs — leaving only the content centered for comfortable, distraction-free reading.

## Features

- Toggle button in the header (next to search)
- Hides navigation, TOC, header, footer, and tabs
- Centers content at a configurable max-width (default: 780px)
- Keyboard shortcut: **Alt+Z** (configurable)
- State persists across pages and reloads via localStorage
- Works with `navigation.instant` (SPA mode)
- Smooth CSS transitions
- Floating exit button when header is hidden
- Fully configurable: choose what to hide
- Dark mode compatible

## Installation

```bash
pip install mkdocs-zen-mode
```

## Quick Start

Add to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - zen-mode
```

That's it! A toggle button will appear in the header.

## Configuration

All options are optional:

```yaml
plugins:
  - zen-mode:
      enabled: true              # Master switch (default: true)
      max_width: "780px"         # Content width in zen mode
      shortcut: "Alt+Z"          # Keyboard shortcut
      storage_key: "mkdocs-zen-mode"  # localStorage key
      button_position: "header"  # "header" or "none"
      hide_header: true          # Hide the top header bar
      hide_footer: true          # Hide the footer
      hide_tabs: true            # Hide navigation tabs
      hide_toc: true             # Hide table of contents (right sidebar)
      hide_nav: true             # Hide navigation (left sidebar)
      hide_announce: true        # Hide the announce bar
      transition_duration: "0.3s"  # CSS transition speed
```

### Examples

Keep the TOC visible in zen mode:

```yaml
plugins:
  - zen-mode:
      hide_toc: false
```

Use a custom keyboard shortcut:

```yaml
plugins:
  - zen-mode:
      shortcut: "Ctrl+Shift+Z"
```

Only use the keyboard shortcut (no visible button):

```yaml
plugins:
  - zen-mode:
      button_position: "none"
```

## Manual Installation (without plugin)

If you prefer not to use the plugin system (or for MkDocs 2.0+), you can manually add the CSS and JS:

1. Copy `mkdocs_zen_mode/assets/zen-mode.css` to `docs/stylesheets/zen-mode.css`
2. Copy `mkdocs_zen_mode/assets/zen-mode.js` to `docs/javascripts/zen-mode.js`
3. Replace the `{{...}}` placeholders in both files with your desired values
4. Add to `mkdocs.yml`:

```yaml
extra_css:
  - stylesheets/zen-mode.css
extra_javascript:
  - javascripts/zen-mode.js
```

5. Add the toggle button to your `overrides/main.html` header block.

## Compatibility

- **MkDocs Material** 9.x (primary target)
- **MkDocs** >= 1.4
- Degrades gracefully on non-Material themes (keyboard shortcut and FAB still work)
- Python 3.9+

## Development

```bash
git clone https://github.com/nitaibezerra/mkdocs-zen-mode.git
cd mkdocs-zen-mode
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT
