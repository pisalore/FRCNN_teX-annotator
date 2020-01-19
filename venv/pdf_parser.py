from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdevice import PDFDevice
import json
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
def parse_pdf(path):
    # Open a PDF file.
    fp = open(path, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    # Set parameters for analysis.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    i = 0
    for page in PDFPage.create_pages(document):
        i += 1
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        print('\n','----------------------------------------------------------------------------------------------------------')
        print('PAGE NUMBER: ', i)
        print('----------------------------------------------------------------------------------------------------------', '\n')
        for x in layout:
            if isinstance(x, LTTextBoxHorizontal):
                results = x.get_text()
                print(results)
            else:
                print(x)

path = '2001.05994.pdf'
parse_pdf(path)