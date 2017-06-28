from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

class Dispatcher:
    def dispatcher(self, prefix, name, attrs=None):
        mname = prefix + name.capitalize()
        dname = 'default' + name.capitalize()
        method = getattr(self, mname, None)
        if callable(method): args=()
        else:
            method = getattr(self, dname, None)
            args = name
        if prefix == 'start': args += attrs
        if callable(method): method(*args)

    def startElement(self, name, attrs):
        self.dispatcher(self, "start", name, attrs)

    def endElement(self, name, attrs):
        self.dispatcher(self, "end", name, attrs)