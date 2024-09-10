# Embed PDF in Sphinx Documentation

## Getting Started

### Installation

Install with pip form github:

```
pip install git+https://github.com/steinerAdi/sphinx-embedPDF.git
```

### Configuration

In your Sphinx ``conf.py`` file add ``sphinx_embedpdf.sphinx_embedpdf`` to the list of extensions.

```
extensions = ['sphinx_embedpdf.sphinx_embedpdf']
```

## Usage

For new-tab links, you can use the inline role:
```
:ntLink:`src:https://www.google.com, name:google, symbol:True`
```

Creating a header with a download symbol, a new-tab link and under the title the embedded PDF with defined size and ratio.

```
.. embedpdf:: ./_static/sample.pdf
    :alt: Alternative text to show pdf is not visible
    :name: Embed PDF Sample
    :width: 95
    :ratio: 75
```