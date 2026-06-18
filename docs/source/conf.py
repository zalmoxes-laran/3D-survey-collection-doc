# Configuration file for the Sphinx documentation builder.

# -- Project information

project = '3D Survey Collection'
copyright = '2023, Simone Berto'
author = 'Simone Berto'

release = '1.5'
version = '1.5.4'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

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
     'Documentation written by Simone Berto',
     'manual'),
]
