from __future__ import annotations

from docutils import nodes

import os
from pathlib import Path

from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata
from sphinx.util import logging

import json

__author__ = "Adrian STEINER"
__version__ = "0.0.1"

logger = logging.getLogger(__name__)
    
def new_tab_link_html(link: str, name = "", symbol = True) -> str:

    if symbol:
        symbolText = '<span class="material-symbols-outlined">open_in_new</span>'
    else:
        symbolText = ""

    htmlText = f'<a href="{link}" target="_blank" rel="noopener noreferrer">{name}{symbolText}</a>'
    return htmlText

def download_html(link: str, name = "", symbol = True) -> str:
    if symbol:
        symbolText = '<span class="material-symbols-outlined">download</span>'
    else:
        symbolText = ''
    
    htmlText = f'<a class="reference download internal" download="" href="{link}">{symbolText}</a>'

    return htmlText

def embed_pdf_html(link: str, ratio: float, width: int, alt: str):
    styleSettings = ""
    if 0 != width:
        styleSettings += f'width:{width}%; '
    if 0 != ratio:
        styleSettings += f'aspect-ratio:{ratio};'

    return f'<div align="center">\
            <object \
            id = "showPDF"\
            type="application/pdf" \
            class="embedpdf"\
            style="{styleSettings}">\
            <p><div align="left">{alt}</p>\
            </object>\
            <script>\
            pdfViewer = document.getElementById("showPDF");\
            pdfViewer.data = PDF_VIEWER.getSrcName("{link}");\
            </script>'
    
def link_newTab(role, rawsource, text, lineno, self):
    text = text.replace(' ', '')
    arguments = {}
    # read specs
    for component in text.split(','):
         arguments[component.split(':')[0]] = component.split(':', 1)[1]
        
    try:
        link = arguments['src']
    except:
        return
    
    try:
        name = arguments['name']
    except:
        name = ""
    
    try:
        withSymbol = eval(arguments['symbol'])
    except:
        withSymbol = True

    if 0 == len(name) and withSymbol is False:
        logger.warning(f"No link name or symbol set for {role}")
    
    node = nodes.raw(text=new_tab_link_html(link=link, name=name, symbol=withSymbol), format='html')
    return [node], []


def headerLink(ref: str) -> str:
    headerLinkHTML = f'<a class="headerlink" href="#{ref}" title="Link to this heading">¶</a>'
    return headerLinkHTML

class PDF_Title_Directive(SphinxDirective):

    required_arguments = 1

    option_spec = {
        "name": directives.unchanged ,
        "hidedownload": directives.flag,
        "hidenewtab": directives.flag,
        "header": directives.nonnegative_int,
        "alt": directives.unchanged,
        "hidepdf": directives.flag,
        "ratio": directives.percentage,
        "width": directives.percentage
    }

    def run(self) -> list[nodes.Node]:

        path = self.arguments[0]
        pdf_name = Path(path).stem

        try:
            name = self.options["name"]
        except:
            name = pdf_name

        try: 
            header = self.options["header"]
        except:
            header = 1

        try: 
            self.options['hidedownload']
            downloadCode = ''
        except:
            downloadCode = download_html(link=path)

        try:
            self.options["hidenewtab"]
            newTabCode = ""
        except:
            newTabCode = new_tab_link_html(path)
        

        headerId = name.replace(" ", "-")

        htmlHeaderCode = f'<h{header} id="{headerId}">{name}{downloadCode}{newTabCode}{headerLink(headerId)}</h{header}>'

        try: 
            alt = self.options["alt"]
        except:
            alt = 'Cannot display PDF, please download it with the link above.'

        try: 
            self.options["hidepdf"]
            pdfCode = ""
        except:
            try:
                ratio = self.options["ratio"]/100
            except:
                ratio = 0
            
            try: 
                width = self.options["width"]
            except:
                width = 0

            pdfCode = embed_pdf_html(path, ratio, width, alt)
            print(pdfCode)

        paragraph_node = nodes.raw(text=htmlHeaderCode+pdfCode, format='html')

        return [nodes.header(), paragraph_node]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive('embedpdf', PDF_Title_Directive)
    app.add_role('ntLink', link_newTab)
    app.add_css_file("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@40,200,0,0")
    app.add_css_file("embedpdf.css")
    app.add_js_file("pdfViewer.js")
    app.config.html_static_path.append(str(Path(__file__).parent.joinpath("resources")))
    
    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

