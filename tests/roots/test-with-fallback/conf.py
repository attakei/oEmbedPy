"""Configuration is cases for default behavior."""

extensions = [
    "oembedpy.adapter.sphinx",
]

# To skip toctree
rst_prolog = """
:orphan:
"""

oembed_fallback_type = True
