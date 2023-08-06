from bs4 import BeautifulSoup
from pyeact.cssgen import CSSObject
from flask import jsonify


class HTMLObject(object):
    content = []
    args = {}
    styles = None

    def __init__(self, tag_name="", args={}, content=[], styles=None):
        self.tag_name = tag_name
        self.args = args
        self.content = content
        if type(styles) == CSSObject:
            self.styles = [styles]
        elif type(styles) == list:
            self.styles = styles

    def __str__(self):
        args_str = ""
        for key, value in self.args.items():
            if key != 'style':
                args_str += f" {key}=\"{value}\""
        style = ' '.join([str(i).replace("_", "-") for i in self.styles])
        args_str += f" style=\"{style}\""
        if type(self.content) != tuple and type(self.content) != list:
            return f"<{self.tag_name}{args_str}>{str(self.content)}</{self.tag_name}>"
        else:
            cnt = ""
            for i in list(self.content):
                cnt += str(i)
            return f"<{self.tag_name}{args_str}>{cnt}</{self.tag_name}>"

    def render(self):
        return self.__str__()


class HTMLGen(object):
    def __getattr__(self, item):
        return lambda args={}, content=[], styles=[]: HTMLObject(item, args, content, styles)


class HTMLPage(object):
    gen = None
    html = None
    head = None
    body = None
    routes = []
    registered_functions = {}

    def __init__(self, routes=['/']):
        self.gen = HTMLGen()
        self.html = self.gen.html()
        self.html.content = []
        head, body = self.gen.head(), self.gen.body()
        self.html.content.append(head)
        self.html.content.append(body)
        self.head = head
        self.head.content.append(self.gen.script({'src': '/bridge.js'}))
        self.body = body
        self.routes = routes

    def __str__(self):
        ret = "<!DOCTYPE html>\n"
        ret += self.html.render()
        return BeautifulSoup(ret, 'lxml').prettify()

    def render(self):
        return str(self)

    def register_function(self, name, function):
        self.registered_functions.update({name: function})


class HTMLBridgeEventGen(object):
    def __init__(self, function_name, function_args):
        self.function_name = function_name
        self.function_args = function_args

    def __str__(self):
        return f"runFunction(\'{self.function_name}\', {self.function_args});"
