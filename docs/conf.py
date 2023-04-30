import os
import sys

sys.path.append(os.path.abspath("../src"))

project = "Pyella"
copyright = "2023, Ely Deckers"
author = "Ely Deckers"

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
