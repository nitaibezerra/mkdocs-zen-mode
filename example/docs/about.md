---
title: About
---

# About mkdocs-zen-mode

A lightweight MkDocs plugin that adds a distraction-free reading mode to sites using the Material theme.

## Why?

Long documentation pages are easier to read without sidebar distractions. Zen Mode gives readers the choice to focus on content when they need to.

## How it works

The plugin uses MkDocs' `on_post_page` hook to inject a small CSS stylesheet and JavaScript snippet into every rendered page. No external dependencies, no build-time processing — just a toggle that adds a CSS class to `<body>`.

### Technical details

- **CSS**: `body.zen-mode-active` class triggers hiding of UI elements via `opacity`, `max-height`, and `pointer-events`
- **JavaScript**: ~2KB, ES5-compatible, handles toggle state, localStorage, keyboard shortcuts, and Material's instant navigation
- **Total overhead**: ~4KB inline per page

## License

MIT License. See [LICENSE](https://github.com/nitaibezerra/mkdocs-zen-mode/blob/main/LICENSE).
