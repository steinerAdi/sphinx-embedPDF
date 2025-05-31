"""
Sphinx embed PDF into websites including controlling the page of the PDF.
@author Adrian STEINER (adi.steiner@hotmail.ch)
@copyright Copyright (c) 2024, 2025 Adrian STEINER
"""

from __future__ import annotations
from docutils import nodes
from pathlib import Path
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata
from sphinx.util import logging
from sphinx.environment import BuildEnvironment

from typing import Tuple
import re
import os

RELATIVE_PATH_TO_STATIC = ""
APP_SRC_DIR = ""

__author__ = "Adrian STEINER"
__version__ = "0.1.0"

logger = logging.getLogger(__name__)


def get_current_rst_file(app: Sphinx, docname: str, source: list):
    """Event handler, which returns the current rst file"""
    static_dir = os.path.commonpath([os.path.abspath(docname), app.srcdir]) + "/_static"
    global APP_SRC_DIR
    APP_SRC_DIR = app.srcdir
    # print("Out dir: ", app.outdir)
    # print("App src dir: ", app.srcdir)
    # print("static dir: ", static_dir)
    # print("static path:", app.config.html_static_path)
    # print("Source: ", source)
    file_dir = os.path.abspath(os.path.dirname(docname))
    global RELATIVE_PATH_TO_STATIC
    RELATIVE_PATH_TO_STATIC = "./" + os.path.relpath(static_dir, file_dir)
    # print("Relative path to static: ", RELATIVE_PATH_TO_STATIC)


def parse_link_role_text(text: str) -> Tuple[str, str, bool]:
    """Pars the link path with the system 'name <link>|<with Symbol>'"""
    parts = text.split("|")
    identity = parts[0].strip()
    with_symbol = parts[1].strip().lower() == "true" if len(parts) > 1 else False

    # Match the text to name <link> rule
    match = re.match(r"^(.*?)\s*<(.+?)>$", identity)
    if match:
        # Link with name
        name = match.group(1).strip()
        link = match.group(2).strip()
    else:
        # No link name, used directly the link without <>
        link = identity
        name = identity

    return [name, link, with_symbol]


# global config variables:
class Global_Config_Type:
    def __init__(self, variable_name: str, default_value):
        self.name = variable_name
        self.default_value = default_value
        self.value = None


class Global_Configs:
    download_symbol = Global_Config_Type("embedpdf_download_symbol", "download")
    newtab_symbol = Global_Config_Type("embedpdf_newtab_symbol", "open_in_new")
    icon_class = Global_Config_Type("embedpdf_icon_class", "material-symbols-outlined")
    zoom = Global_Config_Type("embedpdf_zoom", "auto")
    pagemode = Global_Config_Type("embedpdf_pagemode", "none")
    alt = Global_Config_Type(
        "embedpdf_alt", "Cannot display PDF, please download it with the link above."
    )


global_configs = Global_Configs()


def html_command(command: str, command_features="", text="") -> str:
    if 0 != len(command_features):
        tag_features = " " + command_features
    else:
        tag_features = ""

    return f"<{command}{tag_features}>{text}</{command}>"


def new_tab_link_html(link: str, name="", symbol=True) -> str:
    """Generates the html instructions for a new-tab link"""
    if symbol:
        symbolText = html_command(
            command="span",
            command_features=f'class="{global_configs.icon_class.value}" title="{link}"',
            text=global_configs.newtab_symbol.value,
        )
    else:
        symbolText = ""

    html_text = html_command(
        command="a",
        command_features=f'href="{link}" target="_blank" rel="noopener noreferrer" title="{link}"',
        text=f"{name}{symbolText}",
    )
    html_text = html_command(command="object", text=html_text)
    return html_text


def download_html(link: str, name="", symbol=True) -> str:
    """Generates html instructions for downloads"""
    if symbol:
        symbolText = html_command(
            command="span",
            command_features=f'class="{global_configs.icon_class.value}" title="Download"',
            text=global_configs.download_symbol.value,
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


def embed_pdf_html(
    link: str,
    ratio: float,
    width: int,
    alt: str,
    id: str,
    pageMode="none",
    addClass="",
    zoom="auto",
):
    """Generates the html instructions for an embedded PDF file with pdfjs"""
    styleSettings = ""
    if 0 != width:
        styleSettings += f"width:{width}%; "
    if 0 != ratio:
        styleSettings += f"aspect-ratio:{ratio};"

    pdf_div = (
        html_command("div", command_features=f'id="{id}" align="center"', text=alt)
        + "\n"
    )
    pdf_script = (
        html_command(
            command="script",
            command_features=f'src="{RELATIVE_PATH_TO_STATIC}/pdfViewer.js"',
        )
        + "\n"
    )

    add_PDF_script = (
        html_command(
            "script",
            text=f'addPDFTag("{id}", "../../{link}", "{RELATIVE_PATH_TO_STATIC}/" , "{styleSettings}", "{addClass}", "{pageMode}", "{zoom}")',
        )
        + "\n"
    )

    return pdf_div + pdf_script + add_PDF_script


def link_newTab(role, rawsource, text, lineno, self):
    """Sphinx role callback function to generate a new tab link"""
    [name, link, with_symbol] = parse_link_role_text(text)
    node = nodes.raw(
        text=new_tab_link_html(link=link, name=name, symbol=with_symbol), format="html"
    )
    return [node], []


def download_pdf(role, rawtext, text, lineno, inliner, options={}, content=[]):
    """Sphinx role callback function to generate a download section with a symbol"""
    [name, link, with_symbol] = parse_link_role_text(text)
    link_path = Path(link)
    document_name = Path(inliner.document["source"]).with_suffix('')
    print("Document name: ", document_name)
    env = inliner.document.settings.env

    # Zugriff auf die Sphinx-App
    app = env.app

    # Jetzt kannst du z. B. srcdir holen
    srcdir = app.srcdir
    print("Src dir from download: ", srcdir)
    if link_path.is_absolute():
        link_path = Path(os.path.join(APP_SRC_DIR, str(link_path).lstrip("/")))
    else:
        # Relative path to current file
        print("use relative path ", link_path)
        link_path = Path(os.path.join(document_name, link_path))
    if link_path.is_file():
        print("File exists: ", link_path)
    else:
        logger.warning(f"Download file not readable: {link_path}", location=(str(document_name), int(lineno)))

    node = nodes.raw(
        text=download_html(link=link, name=name, symbol=with_symbol), format="html"
    )
    return [node], []


def header_link(ref: str) -> str:
    header_link_HTML = html_command(
        command="a",
        command_features=f'class="headerlink" href="#{ref}" title="Link to this heading"',
        text="¶",
    )
    return header_link_HTML


class PDF_Title_Directive(SphinxDirective):

    required_arguments = 1

    option_spec = {
        "hideheader": directives.flag,
        "name": directives.unchanged,
        "hidedownload": directives.flag,
        "hidenewtab": directives.flag,
        "headerdepth": directives.nonnegative_int,
        "alt": directives.unchanged,
        "hidepdf": directives.flag,
        "ratio": directives.percentage,
        "width": directives.percentage,
        "pagemode": directives.unchanged,
        "zoom": directives.unchanged,
        "class": directives.unchanged,
    }

    accepted_pagemode_values = {"none", "thumbs", "bookmarks", "attachments"}

    def run(self) -> list[nodes.Node]:

        path = self.arguments[0]
        pdf_name = Path(path).stem

        name = self.options.get("name", pdf_name)
        headerId = name.lower().replace(" ", "-")

        if "hideheader" in self.options:
            htmlHeaderCode = ""
        else:
            header = self.options.get("headerdepth", 1)

            if "hidedownload" in self.options:
                downloadCode = ""
            else:
                downloadCode = download_html(link=f"{RELATIVE_PATH_TO_STATIC}/{path}")

            if "hidenewtab" in self.options:
                newTabCode = ""
            else:
                newTabCode = new_tab_link_html(link=f"{RELATIVE_PATH_TO_STATIC}/{path}")
            # print("PDF Link", {RELATIVE_PATH_TO_STATIC}, "/", {path})
            htmlHeaderCode = html_command(
                f"h{header}",
                command_features=f'id="{headerId}"',
                text=f"{name}{downloadCode}{newTabCode}{header_link(headerId)}",
            )

        alt = self.options.get("alt", global_configs.alt.value)

        if "hidepdf" in self.options:
            pdfCode = ""
        else:

            ratio = self.options.get("ratio", 0) / 100

            width = self.options.get("width", 0)

            pagemode = self.options.get("pagemode", global_configs.pagemode.value)

            if pagemode not in self.accepted_pagemode_values:
                logger.warning(
                    f"pagemode: {pagemode} not allowed.\n Allowed pagemode arguments: {self.accepted_pagemode_values}"
                )
                pagemode = "none"

            zoom = self.options.get("zoom", global_configs.zoom.value)

            additional_class = self.options.get("class", "")

            pdfCode = embed_pdf_html(
                path,
                ratio,
                width,
                alt,
                headerId + "-pdf",
                pageMode=pagemode,
                addClass=additional_class,
                zoom=zoom,
            )

        paragraph_node = nodes.raw(text=htmlHeaderCode + pdfCode, format="html")

        return [nodes.header(), paragraph_node]


def add_embed_pdf_lib(app: Sphinx, env: BuildEnvironment, docnames):
    """Read out all configuration variables"""
    global_configs.download_symbol.value = app.config.embedpdf_download_symbol
    global_configs.newtab_symbol.value = app.config.embedpdf_newtab_symbol
    global_configs.icon_class.value = app.config.embedpdf_icon_class
    global_configs.zoom.value = app.config.embedpdf_zoom
    global_configs.pagemode.value = app.config.embedpdf_pagemode
    global_configs.alt.value = app.config.embedpdf_alt


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("embedpdf", PDF_Title_Directive)
    app.add_role("ntLink", link_newTab)
    app.add_role("download_file", download_pdf)
    app.add_css_file(
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@40,200,0,0"
    )
    app.add_css_file("embedpdf.css")
    app.config.html_static_path.append(str(Path(__file__).parent.joinpath("resources")))
    app.add_config_value(
        name=global_configs.download_symbol.name,
        default=global_configs.download_symbol.default_value,
        rebuild="html",
        description="",
    )
    app.add_config_value(
        global_configs.newtab_symbol.name,
        global_configs.newtab_symbol.default_value,
        "html",
    )
    app.add_config_value(
        global_configs.icon_class.name, global_configs.icon_class.default_value, "html"
    )
    app.add_config_value(
        global_configs.zoom.name, global_configs.zoom.default_value, "html"
    )
    app.add_config_value(
        global_configs.pagemode.name, global_configs.pagemode.default_value, "html"
    )
    app.add_config_value(
        global_configs.alt.name, global_configs.alt.default_value, "html"
    )
    app.connect("env-before-read-docs", add_embed_pdf_lib)
    # app.connect('builder-inited', on_builder_inited)
    app.connect("source-read", get_current_rst_file)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
