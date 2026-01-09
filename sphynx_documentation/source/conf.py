import os
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Documentation du Code'
copyright = '2025, MAIF'
author = 'MAIF'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinxcontrib.matlab', 'sphinx.ext.autodoc', 'sphinx.ext.napoleon',  'sphinx_multiversion']
primary_domain = "mat"

matlab_src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'code_matlab'))
# matlab_src_dir = os.path.abspath('C:/Projets/Interne/MAIF/Documentation_Git_Versioning/documentation_sphynx/code_matlab')
# matlab_src_dir = r'C:\Projets\Interne\MAIF\Documentation_Git_Versioning\documentation_sphynx\code_matlab' 

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
language = 'fr'

# Context for sphinx-multiversion
html_context = {
    'current_version': 'latest',
    'versions': [('latest', '/')],
}
#versioning avec sphinx
smv_tag_whitelist = r'^\d+\.\d+.*$|latest'  # all tags of form *.*.x and latest

# Whitelist pattern for branches (set to '' to ignore all branches)
# smv_branch_whitelist =  r'^.*$'  # all branches
# smv_branch_whitelist =  r'^(master)$' # 
smv_released_pattern = r'^tags/.*$'
smv_latest_version = '0.0.1'
smv_remote_whitelist = r'^origin$'


# html_sidebars = {
#     '**': [
#         'versioning.html',
#     ],
# }