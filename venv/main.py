import glob
import os
from pdf_parser import parse_pdf
from csv_generator import generate_csv_annotations
from csv2txt_converter import obtain_txt_train_images_file
from utils import main_args

PDF_FILES = 'pdf_files/'
TEX_FILES = 'tex_files/'

def main():
    args = main_args()
    is_annotation = args.annotations
    csv_file_path = args.csv_file_path
    num_files = len([f for f in os.listdir(PDF_FILES) if os.path.isfile(os.path.join(PDF_FILES, f))])
    num_train_images = num_files / 100 * 90
    files_processed = 0
    for pdf_file_path in glob.glob(os.path.join(PDF_FILES, '*.pdf')):
        if files_processed < num_train_images:
            is_train = True
            files_processed += 1
        else:
            is_train = False
        file_id = str(os.path.basename(pdf_file_path).split('.pdf')[0])
        tex_file_path = TEX_FILES + file_id + '_tex_files'
        if(os.path.exists(tex_file_path)):
            print('\nParsing ' + pdf_file_path +'...')
            detected_objects = parse_pdf(pdf_file_path, tex_file_path, is_annotation, is_train)
            generate_csv_annotations(csv_file_path, file_id, detected_objects)
            obtain_txt_train_images_file(csv_file_path)


if __name__ == "__main__":
    main()
