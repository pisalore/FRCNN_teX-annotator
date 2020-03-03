import os.path
from pdfminer.layout import LAParams
from pdfminer.layout import LTTextBoxHorizontal, LTFigure, LTImage, LTLine, LTRect
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed
from pdfminer.psparser import PSSyntaxError
from pdf2image_converter import generate_images
from tex_parser import find_tex_istances
from images_annotator import annotate_img
from difflib import SequenceMatcher
from operator import itemgetter
from timeout import timeout

def are_similar(string_a, string_b):
    if SequenceMatcher(None, string_a, string_b).ratio() >= 0.75:
        return True

def calculate_object_coordinates(page_counter, bbox, document_length, obj_category):
    computed_coordinates = []
    computed_coordinates.append(page_counter)

    computed_coordinates.append(bbox[0])
    computed_y_left = document_length - bbox[1]
    computed_coordinates.append(computed_y_left)

    computed_coordinates.append(bbox[2])
    computed_y_right = document_length - bbox[3]
    computed_coordinates.append(computed_y_right)

    computed_coordinates.append(obj_category)

    return computed_coordinates

def clean_Tables(tmp_extracted_tables_coordinates):
    table_id = 0
    lines_counter = 0
    selected_line = tmp_extracted_tables_coordinates[0]
    lines_to_be_removed = []
    for line in tmp_extracted_tables_coordinates[1:]:
        if table_id == line[-1]:
            lines_counter +=1
        elif lines_counter <= 1:
            lines_to_be_removed.append(selected_line)
            lines_counter = 1
        else:
            lines_counter = 1
        table_id = line[-1]
        selected_line = line

    for line_to_be_removed in lines_to_be_removed:
        tmp_extracted_tables_coordinates.remove(line_to_be_removed)
    return tmp_extracted_tables_coordinates

def extract_tables_coordinates(tables_coordinates):
    extracted_tables_coordinates = []
    if(len(tables_coordinates)):
        tmp_extracted_tables_coordinates = []
        added_table_ids = []
        current_page = 1
        current_width = 0
        table_id = 0

        for line in tables_coordinates:
            if line[0] != current_page:
                current_page = line[0]
                current_width = 0
                table_id += 1
            if current_width == 0:
                current_width = line[3] - line[1]
                line.append(table_id)
                tmp_extracted_tables_coordinates.append(line)
            elif abs(current_width - (line[3] - line[1])) <= 1:
                line.append(table_id)
                tmp_extracted_tables_coordinates.append(line)
            else:
                current_width = line[3] - line[1]
                table_id += 1
        tmp_extracted_tables_coordinates = clean_Tables(tmp_extracted_tables_coordinates)
        for i in range(len(tmp_extracted_tables_coordinates)):
            table_id = tmp_extracted_tables_coordinates[i][6]
            page = tmp_extracted_tables_coordinates[i][0]
            table_xmin = []
            table_ymin = []
            table_xmax = []
            table_ymax = []
            for line in tmp_extracted_tables_coordinates:
                if line[6] == table_id and (line[6] not in added_table_ids):
                    table_xmin.append(line[1])
                    table_ymin.append(line[2])
                    table_xmax.append(line[3])
                    table_ymax.append(line[4])
            if table_xmin and table_ymin and table_xmax and table_ymax:
                table_to_add = [page, min(table_xmin), max(table_ymax), max(table_xmax), min(table_ymin), 'table']
                extracted_tables_coordinates.append(table_to_add)
                added_table_ids.append(table_id)

    return extracted_tables_coordinates

def extract_lists_coordinates(items_coordinates):
    items_num = len(items_coordinates)
    extracted_lists_coordinates = []
    if items_num:
        list_found = False
        is_last = False
        are_adjacent = False
        counter = 0
        current_page = items_coordinates[0][0]
        x_p2, y_p2 = items_coordinates[0][1], items_coordinates[0][2]
        x_p1, y_p1 = items_coordinates[0][3], items_coordinates[0][4]
        for item in items_coordinates[1:]:
            counter += 1
            if counter == items_num - 1:
                is_last = True
            if item[0] == current_page:
                if y_p2 >= item[2]:
                    are_adjacent = True
                if abs(y_p2 - item[2]) <= 80 and not are_adjacent:
                    x_p2 = item[1]
                    y_p2 = item[2]
                else:
                    list_found = True
            else:
                list_found = True

            if list_found or is_last:
                list_to_add = [current_page, x_p2, y_p2, x_p1, y_p1, 'list']
                extracted_lists_coordinates.append(list_to_add)
                current_page = item[0]
                x_p2, y_p2 = item[1], item[2]
                x_p1, y_p1 = item[3], item[4]
                list_found = False
                are_adjacent = False

    return extracted_lists_coordinates

@timeout(60)
def parse_pdf(PDF_path, TEX_Path, is_annotation, is_train_image):
    filename = os.path.basename(PDF_path).split('.pdf')[0]
    page_counter = 0
    titles_counter = 0
    titles_coordinates = []
    images_counter = 0
    images_coordinates = []
    lists_coordinates = []
    tables_coordinates = []
    text_coordinates = []
    all_train_objects_coordinates = []
    with_annotations = is_annotation

    #FIRST PHASE: GENERATE IMAGES TO BE ANNOTATED AND EXTRACT ALL TEX ISTANCES INSIDE TEX FILE
    generate_images(PDF_path, filename, is_train_image)

    if is_train_image:
        tex_instances = find_tex_istances(TEX_Path)
        if not tex_instances:
            return all_train_objects_coordinates
        # Open a PDF file.
        fp = open(PDF_path, 'rb')
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        try:
            document = PDFDocument(parser)
        except PSSyntaxError:
            print('Invalid PDF structure')
            return all_train_objects_coordinates

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
                                # print('Title num: ', titles_counter, pdf_line_result)
                                titles_coordinates.append(calculate_object_coordinates(page_counter, lines[i].bbox, page_length, 'title'))
                    lines_counter = 0
                    for i in range(len(lines)):
                        pdf_line_result = lines[i].get_text().split('\n')[0].lower()
                        pdf_line_result = ''.join([i for i in pdf_line_result if not i.isdigit()])

                        for instance in tex_instances[2]:
                            tex_list_item = instance[3]
                            if are_similar(tex_list_item[0:50], pdf_line_result[0:50]) and pdf_line_result != '':
                                lists_coordinates.append(calculate_object_coordinates(page_counter, lines[i].bbox, page_length, 'list'))
                            elif lines_counter > 2:
                                text_coordinates.append(calculate_object_coordinates(page_counter, lines[i].bbox, page_length, 'text'))
                            lines_counter += 1


                #FIGURES
                elif isinstance(x, LTImage) or isinstance(x, LTFigure):
                  #  print('Image num: ', images_counter + 1)            #, tex_instances[1][images_counter][2] verify tex parser for images
                  if (x.width / x.height > 5) or (x.height / x.width >5):
                      pass
                  else:
                      images_counter += 1
                      images_coordinates.append(calculate_object_coordinates(page_counter, x.bbox, page_length, 'image'))

                elif isinstance(x, LTLine):
                    if (x.height == 0 and x.width < 30) or x.width <= 0 :
                        pass
                    else:
                        tables_coordinates.append(calculate_object_coordinates(page_counter, x.bbox, page_length, 'table'))

            extracted_tables_coordinates = extract_tables_coordinates(tables_coordinates)
            extracted_lists_coordinates = extract_lists_coordinates(lists_coordinates)

            if with_annotations == 'yes':
                print('Generating annotations...')
                if len(text_coordinates) != 0: annotate_img(filename, text_coordinates, text_coordinates[0][0], (0, 255, 255), 1)
                if len(titles_coordinates) != 0: annotate_img(filename, titles_coordinates, titles_coordinates[0][0], (0,0,255), 3)
                if len(images_coordinates) != 0: annotate_img(filename, images_coordinates, images_coordinates[0][0], (0,255,0), 3)
                if len(extracted_lists_coordinates) != 0 : annotate_img(filename, extracted_lists_coordinates, extracted_lists_coordinates[0][0], (255,0,0), 3)
                if len(extracted_tables_coordinates) !=0 : annotate_img(filename, extracted_tables_coordinates, extracted_tables_coordinates[0][0], (230, 255, 102), 3)

            all_train_objects_coordinates.extend(titles_coordinates)
            all_train_objects_coordinates.extend(images_coordinates)
            all_train_objects_coordinates.extend(extracted_lists_coordinates)
            all_train_objects_coordinates.extend(extracted_tables_coordinates)
            all_train_objects_coordinates = sorted(all_train_objects_coordinates, key = itemgetter(0))

    return all_train_objects_coordinates