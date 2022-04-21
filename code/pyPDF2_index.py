import sys
from PyPDF2 import PdfFileReader

file = sys.argv[1]

reader = PdfFileReader(file, 'rb')
number_of_pages = reader.numPages
print("Pages: {pages}".format(pages=number_of_pages))

print("Info: {info}".format(info=reader.documentInfo))

# page = reader.pages[0]
page = reader.getPage(0)
contents = page.getContents()
print("Contents: {contents}".format(contents=contents))

text = page.extractText()

print("Text: {}".format(text))