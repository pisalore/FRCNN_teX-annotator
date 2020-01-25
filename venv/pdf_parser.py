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
    if SequenceMatcher(None, string_a, string_b).ratio() >= 0.75:
        return True

def calculate_object_coordinates(bbox, document_length):
    computed_coordinates = []

    computed_y_left = document_length - bbox[1]
    computed_coordinates.append(computed_y_left)
    computed_y_right = document_length - bbox[3]
    computed_coordinates.append(computed_y_right)

    return computed_coordinates



def parse_pdf(PDF_path, TEX_Path):
    page_counter = 0
    titles_counter = 0
    titles_coordinates = []
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
    laparams.line_margin = 0.4
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
                lines = x._objs
                if '' in lines: lines.remove('')
                for i in range(2 if len(lines) > 2 else len(lines)):

                    pdf_title_result = lines[i].get_text().split('\n')[0].lower()
                    pdf_title_result = ''.join([i for i in pdf_title_result if not i.isdigit()])

                    for instance in tex_instances[0]:
                        tex_title = instance[2].lower()
                        if are_similar(tex_title, pdf_title_result) and pdf_title_result != '':
                            titles_counter += 1
                            print(titles_counter, pdf_title_result)
                            titles_coordinates.append(calculate_object_coordinates(lines[i].bbox, 792))

    print(titles_coordinates)



PDF_path = 'pdf_files/2001.05970.pdf'
TEX_path = 'tex_files/2001.05970.tex'
parse_pdf(PDF_path, TEX_path)
