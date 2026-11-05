# Copyright (c) 2025-2026, NVIDIA CORPORATION.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cuML Spark'
copyright = '2025-2026, NVIDIA'
author = 'NVIDIA'
release = '26.06.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    'numpydoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
]

numpydoc_show_class_members = False

autodoc_inherit_docstrings = False

templates_path = ['_templates']
exclude_patterns = []

intersphinx_mapping = {
    'pyspark': ('https://spark.apache.org/docs/latest/api/python', None),
    'cuml': ('https://docs.rapids.ai/api/cuml/stable', None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    'pygments_light_style': 'friendly',
    'pygments_dark_style': 'native',
}
html_static_path = ['_static']
html_css_files = ['vendor/rapids/custom.css', 'cuml-spark.css']
html_js_files = [('vendor/rapids/custom.js', {'defer': 'defer'})]

html_show_sourcelink = False

import inspect
from spark_rapids_ml.utils import _unsupported_methods_attributes

_unsupported_by_class = {}
def autodoc_skip_member(app, what, name, obj, skip, options):
    # adapted from this https://github.com/sphinx-doc/sphinx/issues/9533#issuecomment-962007846
    doc_class=None
    for frame in inspect.stack():
        if frame.function == "get_members":
            doc_class = frame.frame.f_locals["obj"]
            break
    
    exclude = skip
    if doc_class:
        if doc_class not in _unsupported_by_class:
            _unsupported_by_class[doc_class] = _unsupported_methods_attributes(doc_class)

        exclude = name in _unsupported_by_class[doc_class]

    # return True if (skip or exclude) else None  # Can interfere with subsequent skip functions.
    return True if exclude or skip else None

def _write_readable_comments(app, exception):
    """Keep the friendly palette while increasing light-mode comment contrast."""
    if exception is not None or app.builder.format != 'html':
        return

    from pathlib import Path

    from pygments.styles import get_style_by_name
    from pygments.token import Comment
    from pydata_sphinx_theme.pygments import get_pygments_stylesheet

    options = app.config.html_theme_options
    light_style = get_style_by_name(options['pygments_light_style'])

    token_styles = {}
    for token, spec in light_style.styles.items():
        # Sphinx can mutate the raw style definitions on import. Preserve
        # the palette's resolved foreground colors for non-comment tokens.
        foreground = (
            '52636b' if token in Comment
            else light_style.style_for_token(token)['color']
        )
        token_styles[token] = ' '.join(
            '#' + foreground if part.startswith('#') else part
            for part in spec.split()
        )

    class ReadableCommentsStyle(light_style):
        styles = token_styles

    # Run after PyData's CSS generator so the customized palette is included
    # in the generated stylesheet, including in the published API guides.
    css = get_pygments_stylesheet(
        ReadableCommentsStyle, options['pygments_dark_style']
    )
    (Path(app.outdir) / '_static' / 'pygments.css').write_text(css, encoding='utf-8')


def setup(app):
    app.connect('autodoc-skip-member', autodoc_skip_member)
    app.connect('build-finished', _write_readable_comments, priority=800)
