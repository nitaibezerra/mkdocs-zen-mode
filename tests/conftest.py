"""Shared fixtures for mkdocs-zen-mode tests."""

import pytest

# Material 9.x uses <div class="md-search">, older versions use <form class="md-search">
SAMPLE_MATERIAL_HTML = """\
<!doctype html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
</head>
<body dir="ltr" data-md-color-scheme="default">
  <header class="md-header" data-md-component="header">
    <nav class="md-header__inner md-grid">
      <a href="." class="md-header__button md-logo">Logo</a>
      <div class="md-header__title">Title</div>
      <div class="md-search" data-md-component="search" role="dialog">
        <div class="md-search__inner" role="search">
          <form class="md-search__form" name="search">
            <input class="md-search__input" type="text">
          </form>
        </div>
      </div>
      <div class="md-header__source">
        <a href="https://github.com/test/repo">Repo</a>
      </div>
    </nav>
  </header>
  <nav class="md-tabs" data-md-component="tabs">
    <ul class="md-tabs__list">
      <li class="md-tabs__item"><a href="#">Tab</a></li>
    </ul>
  </nav>
  <main class="md-main">
    <div class="md-main__inner md-grid">
      <div class="md-sidebar md-sidebar--primary" data-md-component="sidebar">
        <nav class="md-nav">Navigation</nav>
      </div>
      <div class="md-content">
        <article class="md-content__inner md-typeset">
          <h1>Hello World</h1>
          <p>This is a test page for the zen mode plugin.</p>
        </article>
      </div>
      <div class="md-sidebar md-sidebar--secondary" data-md-component="toc">
        <nav class="md-nav">TOC</nav>
      </div>
    </div>
  </main>
  <footer class="md-footer">
    <div class="md-footer-meta">Footer</div>
  </footer>
  <div class="md-banner">
    <div class="md-banner__inner">Announcement</div>
  </div>
</body>
</html>
"""

# Older Material versions use <form class="md-search"> at top level
SAMPLE_MATERIAL_HTML_LEGACY = """\
<!doctype html>
<html lang="en" class="no-js">
<head>
  <meta charset="utf-8">
  <title>Test Page</title>
</head>
<body dir="ltr">
  <header class="md-header">
    <nav class="md-header__inner md-grid">
      <a href="." class="md-header__button md-logo">Logo</a>
      <form class="md-search" data-md-component="search" role="search">
        <input class="md-search__input" type="text">
      </form>
    </nav>
  </header>
  <main class="md-main">
    <div class="md-main__inner md-grid">
      <div class="md-content">
        <article class="md-content__inner md-typeset">
          <h1>Hello World</h1>
        </article>
      </div>
    </div>
  </main>
</body>
</html>
"""


@pytest.fixture
def sample_html():
    return SAMPLE_MATERIAL_HTML


@pytest.fixture
def sample_html_legacy():
    return SAMPLE_MATERIAL_HTML_LEGACY


@pytest.fixture
def plugin():
    from mkdocs_zen_mode.plugin import ZenModePlugin

    p = ZenModePlugin()
    p.load_config({})
    p.on_config({})
    return p


@pytest.fixture
def disabled_plugin():
    from mkdocs_zen_mode.plugin import ZenModePlugin

    p = ZenModePlugin()
    p.load_config({"enabled": False})
    p.on_config({})
    return p
