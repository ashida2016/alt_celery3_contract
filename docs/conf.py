# Sphinx 文档构建配置（最小化，适配 Read the Docs）。
"""Sphinx 配置。"""

project = "alt_celery3_contract"
author = "alt_celery3_contract"
copyright = "2026, alt_celery3_contract"  # noqa: A001

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

exclude_patterns = ["_build"]
html_theme = "alabaster"
