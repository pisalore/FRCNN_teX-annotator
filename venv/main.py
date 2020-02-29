import glob
import os
from pdf_parser import parse_pdf
from csv_generator import generate_csv_annotations

PDF_FILES = 'pdf_files/'
TEX_FILES = 'tex_files/'

def main():
    num_files = len([f for f in os.listdir(PDF_FILES) if os.path.isfile(os.path.join(PDF_FILES, f))])
    for pdf_file_path in glob.glob(os.path.join(PDF_FILES, '*.pdf')):
        file_id = str(os.path.basename(pdf_file_path).split('.pdf')[0])
        tex_file_path = TEX_FILES + file_id + '_tex_files'
        if(os.path.exists(tex_file_path)):
            print('\nParsing ' + pdf_file_path +'...')
            detected_objects = parse_pdf(pdf_file_path, tex_file_path, num_files)
            generate_csv_annotations('images_annotations', file_id, detected_objects)


if __name__ == "__main__":
    main()
