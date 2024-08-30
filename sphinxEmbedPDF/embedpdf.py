from __future__ import annotations

from docutils import nodes

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective, SphinxRole
from sphinx.util.typing import ExtensionMetadata

import json

class HelloRole(SphinxRole):

    """A role to say hello!"""


    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:

        node = nodes.inline(text=f'Hello {self.text}!')

        return [node], []



class HelloDirective(SphinxDirective):

    """A directive to say hello!"""


    required_arguments = 1


    def run(self) -> list[nodes.Node]:

        paragraph_node = nodes.paragraph(text=f'hello {self.arguments[0]}!')

        return [paragraph_node]
    
def new_tab_link_html(link: str, name = "", symbol = True) -> str:

    if symbol:
        symbolText = '<span class="material-symbols-outlined">open_in_new</span>'
    else:
        symbolText = ""

    htmlText = f'<a href="{link}" target="_blank" rel="noopener noreferrer">{name}{symbolText}</a>'
    print(f"HTML Text: {htmlText}")
    return htmlText
    
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

    if len(name) is 0 and withSymbol is False:
        raise Warning(f"No link name or symbol set for {role}")
    
    node = nodes.raw('', new_tab_link_html(link=link, name=name, symbol=withSymbol), format='html')
    return [node], []

def setup(app: Sphinx) -> ExtensionMetadata:

    app.add_role('hello', HelloRole())
    app.add_directive('hello', HelloDirective)
    app.add_role('ntLink', link_newTab)
    app.add_css_file("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,300,0,0")
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }

