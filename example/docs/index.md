---
title: Home
---

# Welcome to Zen Mode Demo

This is a demo site for the **mkdocs-zen-mode** plugin.

## Try it out

1. Click the **expand icon** in the header (next to search)
2. Or press **Alt+Z** on your keyboard
3. Everything disappears except the content!
4. Click the **floating button** (top-right) or press **Alt+Z** again to exit

## How it works

The plugin injects a small CSS and JavaScript snippet into every page. When activated:

- Navigation sidebar (left) is hidden
- Table of contents (right) is hidden
- Header bar slides up and disappears
- Footer is hidden
- Navigation tabs are hidden
- Content is centered with a comfortable max-width

The state is saved in `localStorage`, so it persists across pages and even browser sessions.

## Configuration

```yaml
plugins:
  - zen-mode:
      max_width: "780px"
      shortcut: "Alt+Z"
      hide_header: true
      hide_footer: true
      hide_tabs: true
      hide_toc: true
      hide_nav: true
```

## Some content to scroll through

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Code example

```python
def fibonacci(n):
    """Generate first n Fibonacci numbers."""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(10):
    print(num)
```

### A table

| Feature | Status |
|---------|--------|
| Toggle button | Implemented |
| Keyboard shortcut | Implemented |
| localStorage persistence | Implemented |
| Instant navigation support | Implemented |
| Dark mode compatible | Implemented |
| Configurable elements | Implemented |
