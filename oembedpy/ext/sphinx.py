"""Sphinx extension module."""

from sphinx.util.logging import getLogger

from ..adapter.sphinx import setup

logger = getLogger(__name__)
logger.warning(f"DEPRECATED: '{__name__}' is moved to 'oembedpy.adapter.sphinx'.")
