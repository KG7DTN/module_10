#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element:
    '''Base Element Class which contains append and render'''

    tag = 'html'
    indent = '    '

    def __init__(self, content=None, **kwargs):
        self.contents = [content]
        self.attributes = kwargs

    def append(self, new_content):
        '''appends new content to the page contents'''
        self.contents.append(new_content)

    def render(self, out_file, ind=""):
        '''base content rendering'''
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
    '''html tag handling'''
    tag = 'html'

    def render(self, out_file, ind=""):
        out_file.write(f"{ind}<!DOCTYPE html>\n")
        super().render(out_file, ind)


class Body(Element):
    '''Body tag handling'''
    tag = 'body'

class P(Element):
    '''paragraph tag handling'''
    tag = 'p'

class Head(Element):
    '''head tag handling'''
    tag = 'head'

class SelfClosingTag(Element):
    '''self closing tags'''
    def __init__(self, **kwargs):
        super().__init__(content=None, **kwargs)

    def render(self, out_file, ind=""):
        attr_str = " ".join(f'{key}="{value}"' for key, value in self.attributes.items())
        if attr_str:
            out_file.write(f"{ind}<{self.tag} {attr_str} />\n")
        else:
            out_file.write(f"{ind}<{self.tag} />\n")

class Meta(SelfClosingTag):
    '''meta tag handling'''
    tag = 'meta'

class Br(SelfClosingTag):
    '''Break tag Handling'''
    tag = "br"

class Hr(SelfClosingTag):
    '''header tag handling'''
    tag = "hr"

class OneLineTag(Element):
    '''one liner handling'''
    def render(self, out_file, ind=""):
        attr_str = ''.join(f' {key}="{value}"' for key, value in self.attributes.items())
        out_file.write(f"{ind}<{self.tag}{attr_str}>")
        if self.contents:
            out_file.write(str(self.contents[0]))
        out_file.write(f"</{self.tag}>\n")

class Title(OneLineTag):
    '''Title tag handling'''
    tag = 'title'

class A(OneLineTag):
    '''attribute handling for links'''
    tag = 'a'

    def __init__(self, link, text):
        super().__init__(text, href=link)

class H(OneLineTag):
    '''header and level tag handling'''
    tag = 'h'

    def __init__(self, level, content):
        self.tag = f'h{level}'
        super().__init__(content)

class Ul(Element):
    '''unstructured list handling'''
    tag = 'ul'

class Li(Ul):
    '''list handling'''
    tag = 'li'
