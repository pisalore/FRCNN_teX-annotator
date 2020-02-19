from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal, LTFigure, LTImage, LTLine, LTRect
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
import os.path

from pdf2image_converter import generate_images
from tex_parser import find_tex_istances
from images_annotator import annotate_img
from difflib import SequenceMatcher
def are_similar(string_a, string_b):
    if SequenceMatcher(None, string_a, string_b).ratio() >= 0.75:
        return True

def calculate_object_coordinates(page_counter, bbox, document_length):
    computed_coordinates = []
    computed_coordinates.append(page_counter)

    computed_coordinates.append(bbox[0])
    computed_y_left = document_length - bbox[1]
    computed_coordinates.append(computed_y_left)

    computed_coordinates.append(bbox[2])
    computed_y_right = document_length - bbox[3]
    computed_coordinates.append(computed_y_right)

    return computed_coordinates

def parse_pdf(PDF_path, TEX_Path):
    filename = os.path.basename(PDF_path).split('.pdf')[0]

    page_counter = 0
    titles_counter = 0
    titles_coordinates = []

    images_counter = 0
    images_coordinates = []

    list_id = 0
    current_list = 1
    current_list_items = []
    lists_coordinates = []


    tables_coordinates = []
    #FIRST PHASE: GENERATE IMAGES TO BE ANNOTATED AND EXTRACT ALL TEX ISTANCES INSIDE TEX FILE
    generate_images(PDF_path, filename)
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
        page_length = page.mediabox[3]

        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        print('##########################################################################################################')
        print('PAGE NUMBER: ', page_counter)
        print('##########################################################################################################', '\n')
        for x in layout:
            # TEXTS (TITLES AND LISTS)
            if isinstance(x, LTTextBoxHorizontal):
                lines = x._objs
                if '' in lines: lines.remove('')
                for i in range(2 if len(lines) > 2 else len(lines)): #iterate over the first lines of a texbox since titles are always on the top

                    pdf_line_result = lines[i].get_text().split('\n')[0].lower()
                    pdf_line_result = ''.join([i for i in pdf_line_result if not i.isdigit()])

                    for instance in tex_instances[0]:
                        tex_title = instance[2].lower()
                        if are_similar(tex_title, pdf_line_result) and pdf_line_result != '':
                            titles_counter += 1
                            titles_found = True
                            # print('Title num: ', titles_counter, pdf_line_result)
                            titles_coordinates.append(calculate_object_coordinates(page_counter, lines[i].bbox, page_length))

                for i in range(len(lines)):
                    pdf_line_result = lines[i].get_text().split('\n')[0].lower()
                    pdf_line_result = ''.join([i for i in pdf_line_result if not i.isdigit()])

                    for instance in tex_instances[2]:
                        tex_list_item = instance[3]
                        if are_similar(tex_list_item[0:50], pdf_line_result[0:50]) and pdf_line_result != '':
                            lists_coordinates.append(calculate_object_coordinates(page_counter, lines[i].bbox, page_length))

            #FIGURES
            elif isinstance(x, LTImage) or isinstance(x, LTFigure):
              #  print('Image num: ', images_counter + 1)            #, tex_instances[1][images_counter][2] verify tex parser for images
              if (x.width / x.height > 5) or (x.height / x.width >5):
                  pass
              else:
                  images_counter += 1
                  images_coordinates.append(calculate_object_coordinates(page_counter, x.bbox, page_length))

            elif isinstance(x, LTLine):
                if (x.height == 0 and x.width < 30) or (x.height < 30 and x.width == 0) :
                    pass
                else:
                    tables_coordinates.append(calculate_object_coordinates(page_counter,x.bbox, page_length))

    if len(titles_coordinates) != 0: annotate_img(filename, titles_coordinates, titles_coordinates[0][0], (0,0,255))
    if len(images_coordinates) != 0: annotate_img(filename, images_coordinates, images_coordinates[0][0], (0,255,0))
    if len(lists_coordinates) != 0 : annotate_img(filename, lists_coordinates, lists_coordinates[0][0], (255,0,0))
    if len(tables_coordinates) !=0 : annotate_img(filename, tables_coordinates, tables_coordinates[0][0], (230, 255, 102))

#parse_pdf('pdf_files/1901.0401.pdf', 'tex_files/1901.0401_tex_files')