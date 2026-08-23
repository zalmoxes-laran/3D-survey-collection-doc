# Configuration file for the Sphinx documentation builder.

# -- Project information

project = '3D Survey Collection'
copyright = '2024, Emanuel Demetrescu, Simone Berto'
author = 'Emanuel Demetrescu, Simone Berto'

release = '1.7'
version = '1.7.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    # `_includes/` is the canonical home of reusable RST snippets pulled
    # in via `.. include:: /_includes/<file>.rst`. Excluding it keeps the
    # snippets consumable but unindexed so Sphinx doesn't parse them as
    # orphan standalone documents.
    '_includes/**',
]

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Enable numref
numfig = True
# -- PDF (LaTeX) cover -------------------------------------------------
# Make explicit that this is the *documentation*, credited to its own
# author(s) (4th tuple field = the name printed on the PDF cover), so it
# is not mistaken for the software's author.
latex_documents = [
    ('index', '3DSurveyCollection.tex',
     f'{project} Documentation',
     'Documentation written by Emanuel Demetrescu and Simone Berto',
     'manual'),
]

# -- AI Act Article 50 transparency footer -----------------------------
# A short notice appended to every page via ``rst_epilog``, pointing to
# the project's AI usage policy at extendedmatrix.org/ai-usage/. This
# documentation qualifies for the human-review-and-editorial-
# responsibility exception in Art. 50(4) of Regulation (EU) 2024/1689
# (AI Act); the footer is added for traceability.
rst_epilog = """
.. include:: /_includes/ai_usage_notice.rst
"""
