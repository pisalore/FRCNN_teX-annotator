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
from tex_parser import find_tex_istances
from difflib import SequenceMatcher

def are_similar(string_a, string_b):
    if SequenceMatcher(None, string_a, string_b).ratio() >= 0.7:
        return True


def parse_pdf(PDF_path, TEX_Path):
    page_counter = 0
    titles_counter = 0
    titles_coordinates = []
    all_titles_found = False
    #FIRST PHASE: EXTRACT ALL TEX ISTANCES INSIDE TEX FILE
    tex_instances = find_tex_istances(TEX_Path)
    # Open a PDF file.
    fp = open(PDF_path, 'rb')
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
    laparams.line_margin = 0.2
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(document):
        page_counter += 1
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        print('\n','----------------------------------------------------------------------------------------------------------')
        print('PAGE NUMBER: ', page_counter)
        print('----------------------------------------------------------------------------------------------------------', '\n')
        for x in layout:
            if isinstance(x, LTTextBoxHorizontal):
                if not all_titles_found:
                    if len(x.get_text().replace('\n', '').replace(' ', '')) > 5:
                        pdf_title_result = x.get_text().split('\n')[0].lower()
                        pdf_title_result = ''.join([i for i in pdf_title_result if not i.isdigit()])
                        istance_to_remove = None
                        for instance in tex_instances[0]:
                            #tex_title = tex_istances[0][titles_counter][2].lower()
                            if are_similar(instance[2].lower(), pdf_title_result) and pdf_title_result != '':
                                print (pdf_title_result)
                                titles_counter += 1
                                istance_to_remove = instance
                                if titles_counter == len(tex_instances[0]):
                                    all_titles_found = True
                        if(istance_to_remove is not None):
                            tex_instances[0].remove(istance_to_remove)

PDF_path = '2001.05994.pdf'
TEX_path = '2001.05994.tex'
parse_pdf(PDF_path, TEX_path)
