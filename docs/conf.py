# noqa: D100
project = "oEmbedPy"
copyright = "2023, Kazuya Takei"
author = "Kazuya Takei"

extensions = [
    "oembedpy.ext.sphinx",
    "rst_package_refs.sphinx",
    "sphinx.ext.autodoc",
    "sphinx_toolbox.confval",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]
html_extra_path = ["_extra"]

# -- Options for Linkcheck output
linkcheck_ignore = [
    "../../demo/mkdocs/",
]
