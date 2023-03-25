# noqa: D100
project = "oEmbedPy"
copyright = "2023, Kazuya Takei"
author = "Kazuya Takei"

extensions = [
    "oembedpy.ext.sphinx",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]
