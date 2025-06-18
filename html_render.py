#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element:

    tag = 'html'
    indent = '    '

    def __init__(self, content=None, **kwargs):
        self.contents = [content]
        self.attributes = kwargs

    def append(self, new_content):
        self.contents.append(new_content)

    def render(self, out_file, ind=""):
        if not self.attributes:
            out_file.write(f"{ind}<{self.tag}>\n")
        else:
            attributes = ' '.join(f'{key}="{value}"' for key, value in self.attributes.items())
            out_file.write(f"{ind}<{self.tag} {attributes}>\n")
        for content in self.contents:
            if hasattr(content, 'render'):
                content.render(out_file, ind + self.indent)
            else:
                if content is not None:
                    out_file.write(f'{ind + self.indent}{content}\n')
        out_file.write(f"{ind}</{self.tag}>\n")

class Html(Element):
    tag = 'html'

    def render(self, out_file, ind=""):
        out_file.write(f"{ind}<!DOCTYPE html>\n")
        super().render(out_file, ind)


class Body(Element):
    tag = 'body'

class P(Element):
    tag = 'p'

class Head(Element):
    tag = 'head'

class SelfClosingTag(Element):
    def __init__(self, **kwargs):
        super().__init__(content=None, **kwargs)

    def render(self, out_file, ind=""):
        attr_str = " ".join(f'{key}="{value}"' for key, value in self.attributes.items())
        if attr_str:
            out_file.write(f"{ind}<{self.tag} {attr_str} />\n")
        else:
            out_file.write(f"{ind}<{self.tag} />\n")

class Br(SelfClosingTag):
    tag = "br"

class Hr(Element):
    tag = "hr"

class OneLineTag(Element):
    def render(self, out_file, ind=""):
        for content in self.contents:
            if hasattr(content, 'render'):
                content.render(f'{ind}out_file')
            else:
                if content is not None:
                    out_file.write(f"{ind}<{self.tag}>{content}</{self.tag}>\n")

class Title(OneLineTag):
    tag = 'title'
