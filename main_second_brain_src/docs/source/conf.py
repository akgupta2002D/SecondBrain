import os
import sys
import django

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Second_Brain'
copyright = '2024, Ankit K Gupta'
author = 'Ankit K Gupta'
release = '1.0'

# Base Directory to search:

# Path to your Django project
sys.path.insert(0, os.path.abspath('../..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'main_app.settings'
django.setup()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
    'myst_parser',
    'sphinx_markdown_tables',
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']


# Use Google style docstrings rather than NumPy style
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# Autodoc config
autodoc_member_order = 'bysource'
autodoc_typehints = 'none'


autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__init__',
    'exclude-members': 'DoesNotExist, MultipleObjectsReturned'
}
