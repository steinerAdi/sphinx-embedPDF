"""
Sphinx embed PDF into websites including controlling the page of the PDF.
@author Adrian STEINER
@copyright Copyright (c) 2024 Adrian STEINER under MIT
"""

from __future__ import annotations
from docutils import nodes
from pathlib import Path
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata
from sphinx.util import logging

__author__ = "Adrian STEINER"
__version__ = "0.0.1"

logger = logging.getLogger(__name__)


def html_command(command: str, command_features="", text="") -> str:
    return f"<{command} {command_features}>{text}</{command}>"


def new_tab_link_html(link: str, name="", symbol=True) -> str:
    if symbol:
        symbolText = html_command(
            command="span",
            command_features='class="material-symbols-outlined" title="Open in new tab"',
            text="open_in_new",
        )
    else:
        symbolText = ""

    html_text = html_command(
        command="a",
        command_features=f'href="{link}" target="_blank" rel="noopener noreferrer"',
        text=f"{name}{symbolText}",
    )
    html_text = html_command(command="object", text=html_text)
    return html_text


def download_html(link: str, name="", symbol=True) -> str:
    if symbol:
        symbolText = html_command(
            command="span",
            command_features='class="material-symbols-outlined" title="Download"',
            text="download",
        )
    else:
        symbolText = ""

    html_text = html_command(
        command="a",
        command_features=f'class="reference download internal" download="" href="{link}"',
        text=f"{name}{symbolText}",
    )
    html_text = html_command(command="object", text=html_text)
    return html_text


def embed_pdf_html(link: str, ratio: float, width: int, alt: str, id: str):
    styleSettings = ""
    if 0 != width:
        styleSettings += f"width:{width}%; "
    if 0 != ratio:
        styleSettings += f"aspect-ratio:{ratio};"
    embed_script =  html_command(command='script', command_features='src="/_static/pdfViewer.js"')
    embed_script += html_command(
        command="script",
        text=f'pdfViewer = document.getElementById("{id}"); pdfViewer.data = PDF_VIEWER.getSrcName("{link}");',
    )
    embed_script = f'<iframe class="embedpdf" title="Embedded PDF" src="/_static/pdfjs/web/viewer.html?file={link}#page=;pagemode=none" allow="fullscreen" style="{styleSettings}"></iframe>'

    print(embed_script)
    alternate_text = html_command(command="div", command_features='align="left"', text=alt)
    alternate_text = html_command(command="p", text=alternate_text)
    embed_html = html_command(
        command="object",
        command_features=f'id = "{id}" type="application/pdf" class="embedpdf" style="{styleSettings}"',
        text=alternate_text,
    )
    total_html = html_command(
        command="div", command_features='align="center"', text=embed_html + embed_script
    )
    return total_html


def link_newTab(role, rawsource, text, lineno, self):
    text = text.replace(" ", "")
    arguments = {}
    # read specs
    for component in text.split(","):
        arguments[component.split(":")[0]] = component.split(":", 1)[1]

    link = arguments.get("src", None)

    if link is None:
        logger.error(f"No src:link set for {rawsource} at line {lineno}")
        return [nodes.raw()], []

    name = arguments.get("name", "")
    withSymbol = bool(int(arguments.get("symbol", 1)))

    if 0 == len(name) and withSymbol is False:
        logger.warning(f"No link name or symbol set for {rawsource} at line {lineno}")

    node = nodes.raw(
        text=new_tab_link_html(link=link, name=name, symbol=withSymbol), format="html"
    )
    return [node], []


def download_pdf(role, rawsource, text, lineno, self):

    text = text.replace(" ", "")
    arguments = {}
    # read specs
    for component in text.split(","):
        arguments[component.split(":")[0]] = component.split(":", 1)[1]

    link = arguments.get("src", None)

    if link is None:
        logger.error(f"No src:link set for {rawsource} at line {lineno}")
        return

    link = arguments.get("src", None)

    if link is None:
        logger.warning(f"No src link set for {rawsource} at line {lineno}")
        return

    name = arguments.get("name", "")
    withSymbol = bool(int(arguments.get("symbol", 1)))

    if 0 == len(name) and withSymbol is False:
        logger.warning(f"No link name or symbol set for {rawsource} at line {lineno}")

    node = nodes.raw(
        text=download_html(link=link, name=name, symbol=withSymbol), format="html"
    )
    return [node], []


def headerLink(ref: str) -> str:
    headerLinkHTML = (
        f'<a class="headerlink" href="#{ref}" title="Link to this heading">¶</a>'
    )
    return headerLinkHTML


class PDF_Title_Directive(SphinxDirective):

    required_arguments = 1

    option_spec = {
        "name": directives.unchanged,
        "hidedownload": directives.flag,
        "hidenewtab": directives.flag,
        "header": directives.nonnegative_int,
        "alt": directives.unchanged,
        "hidepdf": directives.flag,
        "ratio": directives.percentage,
        "width": directives.percentage,
        "addtoheader": directives.flag,
    }

    def run(self) -> list[nodes.Node]:

        path = self.arguments[0]
        pdf_name = Path(path).stem

        name = self.options.get("name", pdf_name)
        header = self.options.get("header", 1)

        try:
            self.options["hidedownload"]
            downloadCode = ""
        except:
            downloadCode = download_html(link=path)

        try:
            self.options["hidenewtab"]
            newTabCode = ""
        except:
            newTabCode = new_tab_link_html(path)

        headerId =  name.lower().replace(" ", "-")
        if "addtoheader" in self.options:
            htmlHeaderCode = f'<h{header} id="{headerId}">{name}{downloadCode}{newTabCode}{headerLink(headerId)}</h{header}>'
        else:
            htmlHeaderCode = ""

        alt = self.options.get(
            "alt", "Cannot display PDF, please download it with the link above."
        )

        try:
            self.options["hidepdf"]
            pdfCode = ""
        except:
            try:
                ratio = self.options["ratio"] / 100
            except:
                ratio = 0

            try:
                width = self.options["width"]
            except:
                width = 0

            pdfCode = embed_pdf_html(path, ratio, width, alt, headerId+'-pdf')

        paragraph_node = nodes.raw(text=htmlHeaderCode + pdfCode, format="html")

        return [nodes.header(), paragraph_node]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("embedpdf", PDF_Title_Directive)
    app.add_role("ntLink", link_newTab)
    app.add_role("downloadPDF", download_pdf)
    app.add_css_file(
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@40,200,0,0"
    )
    app.add_css_file("embedpdf.css")
    app.config.html_static_path.append(str(Path(__file__).parent.joinpath("resources")))

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
