---
title: Configuration
---

# Configuration

All configuration options with their defaults:

```yaml
plugins:
  - zen-mode:
      enabled: true
      max_width: "780px"
      shortcut: "Alt+Z"
      storage_key: "mkdocs-zen-mode"
      button_position: "header"
      hide_header: true
      hide_footer: true
      hide_tabs: true
      hide_toc: true
      hide_nav: true
      transition_duration: "0.3s"
```

## Options

### `enabled`

Master switch. Set to `false` to completely disable the plugin.

### `max_width`

The maximum width of the content area when Zen Mode is active. Default is `780px`, which is comfortable for reading.

### `shortcut`

Keyboard shortcut to toggle Zen Mode. Supports modifier keys: `Alt`, `Ctrl`, `Shift`, `Meta`.

Examples: `Alt+Z`, `Ctrl+Shift+Z`, `Meta+Z`

### `storage_key`

The localStorage key used to persist the Zen Mode state. Change this if you have multiple MkDocs sites on the same domain.

### `button_position`

- `header` (default): Show toggle button in the header
- `none`: No visible button (use keyboard shortcut only)

### `hide_*` options

Each `hide_*` option controls whether a specific UI element is hidden:

| Option | Element | CSS Selector |
|--------|---------|-------------|
| `hide_nav` | Left sidebar | `.md-sidebar--primary` |
| `hide_toc` | Right sidebar (TOC) | `.md-sidebar--secondary` |
| `hide_header` | Top header bar | `.md-header` |
| `hide_footer` | Footer | `.md-footer` |
| `hide_tabs` | Navigation tabs | `.md-tabs` |

### `transition_duration`

CSS transition duration for showing/hiding elements. Set to `0s` for instant toggle.
