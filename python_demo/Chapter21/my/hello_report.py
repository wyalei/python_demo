from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF

d = Drawing(100, 100)
s = String(50, 50, 'xiang yan li hao neng gan!', textAnchor='middle')

d.add(s)
renderPDF.drawToFile(d, 'hello2.pdf', 'a simple pdf file')