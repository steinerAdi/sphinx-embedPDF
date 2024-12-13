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
from sphinx.environment import BuildEnvironment

import os

RELATIVE_PATH_TO_STATIC = ''

__author__ = "Adrian STEINER"
__version__ = "0.0.1"

logger = logging.getLogger(__name__)

def get_current_rst_file(app: Sphinx, docname: str, source: list):
    """Event handler, der das aktuell bearbeitete .rst-File ausgibt."""
    # print(f"Current working .rst-File: {docname}.rst")
    # print(os.path.abspath(docname))
    static_dir = os.path.commonpath([os.path.abspath(docname), app.srcdir]) + '/_static'
    file_dir = os.path.abspath(os.path.dirname(docname))
    #print(static_dir)
    #print(file_dir)
    global RELATIVE_PATH_TO_STATIC
    RELATIVE_PATH_TO_STATIC = './' + os.path.relpath(static_dir, file_dir)
    #print(RELATIVE_PATH_TO_STATIC)

# global config variables:
class Global_Config_Type():
    def __init__(self, variable_name: str, default_value):
        self.name = variable_name
        self.default_value = default_value
        self.value = None

class Global_Configs():
    download_symbol = Global_Config_Type("embedpdf_download_symbol", "download")
    newtab_symbol = Global_Config_Type("embedpdf_newtab_symbol", "open_in_new")
    icon_class = Global_Config_Type("embedpdf_icon_class", "material-symbols-outlined")
    zoom = Global_Config_Type("embedpdf_zoom", "auto")
    pagemode =  Global_Config_Type("embedpdf_pagemode", "none")
    alt =Global_Config_Type("embedpdf_alt", "Cannot display PDF, please download it with the link above.")

global_configs = Global_Configs()


def html_command(command: str, command_features="", text="") -> str:
    if 0 != len(command_features):
        tag_features = " "+command_features
    else:
        tag_features = ""
        
    return f"<{command}{tag_features}>{text}</{command}>"


def new_tab_link_html(link: str, name="", symbol=True) -> str:
    if symbol:
        symbolText = html_command(
            command="span",
            command_features=f'class="{global_configs.icon_class.value}" title="Open in new tab"',
            text=global_configs.newtab_symbol.value
        )
    else:
        symbolText = ""

    html_text = html_command(
        command='a',
        command_features=f'href="{link}" target="_blank" rel="noopener noreferrer"',
        text=f"{name}{symbolText}",
    )
    html_text = html_command(command="object", text=html_text)
    return html_text


def download_html(link: str, name="", symbol=True) -> str:
    if symbol:
        symbolText = html_command(
            command="span",
            command_features=f'class="{global_configs.icon_class.value}" title="Download"',
            text= global_configs.download_symbol.value
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


def embed_pdf_html(link: str, ratio: float, width: int, alt: str, id: str, pageMode="none", addClass="", zoom = "auto"):
    styleSettings = ""
    if 0 != width:
        styleSettings += f"width:{width}%; "
    if 0 != ratio:
        styleSettings += f"aspect-ratio:{ratio};"

    # Absoluten Pfad zur aktuellen Datei ermitteln
    # current_file_path = os.path.abspath(__file__)

    # # Relativen Pfad zu einem anderen Verzeichnis (z.B. zum _static Ordner)
    # relative_path = os.path.join(os.path.dirname(current_file_path), '_static')

    #print(f"Current path: {current_file_path} Relativer Pfad: {relative_path}")

    pdf_div = html_command('div', command_features=f'id="{id}" align="center"', text=alt) + '\n'
    pdf_script = html_command(command='script', command_features=f'src="{RELATIVE_PATH_TO_STATIC}/pdfViewer.js"') + '\n'
    # print(RELATIVE_PATH_TO_STATIC)
    add_PDF_script = html_command('script', text=f'addPDFTag("{id}", "../../{link}", "{RELATIVE_PATH_TO_STATIC}/" , "{styleSettings}", "{addClass}", "{pageMode}", "{zoom}")') + '\n'

    return pdf_div + pdf_script + add_PDF_script


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
    
    node = nodes.raw(text=new_tab_link_html(
        link=link, name=name, symbol=withSymbol), format="html")
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
    headerLinkHTML = html_command( 
        command='a', 
        command_features=f'class="headerlink" href="#{ref}" title="Link to this heading"',
        text='¶'
    )
    return headerLinkHTML


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
        "class": directives.unchanged
    }

    accepted_pagemode_values = {
        'none', 'thumbs', 'bookmarks', 'attachments'
    }

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
                downloadCode = download_html(link=path)

            if "hidenewtab" in self.options:
                newTabCode = ""
            else:
                newTabCode = new_tab_link_html(path)

            htmlHeaderCode = html_command(f'h{header}', command_features=f'id="{headerId}"', text=f'{name}{downloadCode}{newTabCode}{headerLink(headerId)}')


        alt = self.options.get(
            "alt", global_configs.alt.value
        )

        if "hidepdf" in self.options:
            pdfCode = ""
        else:

            ratio = self.options.get("ratio", 0) / 100

            width = self.options.get("width", 0) 

            pagemode = self.options.get("pagemode", global_configs.pagemode.value)

            if pagemode not in self.accepted_pagemode_values:
                logger.warning(f'pagemode: {pagemode} not allowed.\n Allowed pagemode arguments: {self.accepted_pagemode_values}')
                pagemode = "none"
            
            zoom = self.options.get("zoom", global_configs.zoom.value)

            additional_class = self.options.get("class", "")

            pdfCode = embed_pdf_html(path, ratio, width, alt, headerId+'-pdf', pageMode=pagemode, addClass=additional_class, zoom=zoom)

        paragraph_node = nodes.raw(text=htmlHeaderCode + pdfCode, format="html")

        return [nodes.header(), paragraph_node]

def add_embed_pdf_lib(app: Sphinx, env: BuildEnvironment, docnames):
    global_configs.download_symbol.value = app.config.embedpdf_download_symbol
    global_configs.newtab_symbol.value = app.config.embedpdf_newtab_symbol
    global_configs.icon_class.value = app.config.embedpdf_icon_class
    global_configs.zoom.value = app.config.embedpdf_zoom
    global_configs.pagemode.value = app.config.embedpdf_pagemode
    global_configs.alt.value = app.config.embedpdf_alt

def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("embedpdf", PDF_Title_Directive)
    app.add_role("ntLink", link_newTab)
    app.add_role("downloadPDF", download_pdf)
    app.add_css_file(
        "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@40,200,0,0"
    )
    app.add_css_file("embedpdf.css")
    app.config.html_static_path.append(str(Path(__file__).parent.joinpath("resources")))
    app.add_config_value(name=global_configs.download_symbol.name, default=global_configs.download_symbol.default_value, rebuild='html', description="glog")
    app.add_config_value(global_configs.newtab_symbol.name, global_configs.newtab_symbol.default_value, 'html')
    app.add_config_value(global_configs.icon_class.name, global_configs.icon_class.default_value, 'html')
    app.add_config_value(global_configs.zoom.name, global_configs.zoom.default_value, 'html')
    app.add_config_value(global_configs.pagemode.name, global_configs.pagemode.default_value, 'html')
    app.add_config_value(global_configs.alt.name, global_configs.alt.default_value, 'html')
    app.connect('env-before-read-docs', add_embed_pdf_lib)
    #app.connect('builder-inited', on_builder_inited)
    app.connect('source-read', get_current_rst_file)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
