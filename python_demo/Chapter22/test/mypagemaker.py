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

class WebsiteContructor(Dispatcher, ContentHandler):

    passthrough = False
    def __init__(self, dir):
        self.dirctory = [dir]
        self.ensureDirctory()

    def ensureDirctory(self):
        path = os.path.join(*self.dirctory)
        os.mkdir(path, exist_ok=True)

    

    def startPage(self, attrs):
        passthrough = True
        path = os.path.join(*self.dirctory + attrs['name'] + ".html")
        self.out = open(path, 'w')
        self.writeTitle(attrs['title'])

    def endPage(self):
        self.writeFooter()
        self.out.close()
        passthrough = False

    def writeTitle(self, title):
        self.out.write("<html>\n<title>\n")
        self.out.write(title)
        self.out.write("\n</title>\n<body>")

    def writeFooter(self):
        self.out.write("</body>\n</html>")