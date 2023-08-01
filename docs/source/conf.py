# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'heuristics_and_routing')))
sys.path.insert(0, os.path.abspath(os.path.join('..', '..', 'heuristics_and_routing', 'heuristics')))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Public_Python_Sim'
copyright = '2022, Alexander Masterman'
author = 'Alexander Masterman'
release = '0.5 Alpha'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon'

]

templates_path = ['_templates']
exclude_patterns = []

#Mock Imports
autodoc_mock_imports = ['tkinter', 'numpy']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'agogo'
html_static_path = ['static']
