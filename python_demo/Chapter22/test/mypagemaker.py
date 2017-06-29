from xml.sax.handler import ContentHandler
from xml.sax import parse
import os

class Dispatcher:
    def dispatch(self, prefix, name, attrs=None):
        mname = prefix + name.capitalize()
        dname = 'default' + prefix.capitalize()
        method = getattr(self, mname, None)
        if callable(method): args=()
        else:
            method = getattr(self, dname, None)
            args = name,
        if prefix == 'start': args += attrs,
        if callable(method): method(*args)

    def startElement(self, name, attrs):
        self.dispatch("start", name, attrs)

    def endElement(self, name):
        self.dispatch("end", name)

class WebsiteContructor(Dispatcher, ContentHandler):

    passthrough = False

    def __init__(self, directory):
        self.directory = [directory]
        self.ensureDirectory()

    def ensureDirectory(self):
        path = os.path.join(*self.directory)
        os.makedirs(path, exist_ok=True)

    def characters(self, content):
        if self.passthrough:
            self.out.write(content)

    def defaultStart(self, name, attrs):
        if self.passthrough:
            self.out.write("<" + name)
            for key, val in attrs.items():
                self.out.write(' {}="{}"'.format(key, val))
            self.out.write(">")

    def defaultEnd(self, name):
        if self.passthrough:
            self.out.write("</{}>".format(name))

    def startDirectory(self, attrs):
        self.directory.append(attrs['name'])
        self.ensureDirectory()

    def endDirectory(self):
        self.directory.pop()

    def startPage(self, attrs):
        path = os.path.join(*self.directory + [attrs['name'] + ".html"])
        self.out = open(path, 'w')
        self.writeTitle(attrs['title'])
        self.passthrough = True

    def endPage(self):
        self.passthrough = False
        self.writeFooter()
        self.out.close()

    def writeTitle(self, title):
        self.out.write("<html>\n<title>\n")
        self.out.write(title)
        self.out.write("\n</title>\n<body>")

    def writeFooter(self):
        self.out.write("</body>\n</html>")

parse("website.xml", WebsiteContructor("html_result"))