# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

project = 'Embed PDF Doc'
copyright = '2024, Adrian STEINER'
author = 'Adrian STEINER'
version = 'v0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

sys.path.append(os.path.abspath("../../sphinxEmbedPDF/"))
extensions = ['sphinx_embedpdf',
              'sphinx_copybutton',
              'sphinx_rtd_theme']

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_favicon = '_static/favicon.png'
#html_logo = html_favicon

html_context = {
    "display_github": True, # Integrate GitHub
    "github_user": "steinerAdi", # Username
    "github_repo": "sphinx-embedPDF", # Repo name
    "github_version": "develop", # Version
    "conf_py_path": "/doc/source/", # Path in the checkout to the docs root
}

html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': True,
#    'vcs_pageview_mode': 'display_github',
#    'style_nav_header_background': 'black',
#    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
#    'titles_only': False
}

