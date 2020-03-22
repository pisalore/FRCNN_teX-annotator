import os
from pdf_parser import parse_pdf
from csv_generator import generate_csv_annotations
from csv2txt_converter import obtain_txt_train_images_file

test_imgs_path = './png_files/test_images'
pdf_files = './pdf_files/'
tex_files = './tex_files/'
csv_file_path = 'test_images_annotations.csv'
txt_path = 'frcnn/annotated_test_images.txt'
list_subfolders = [f.path for f in os.scandir(test_imgs_path) if f.is_dir()]
for subdir in list_subfolders:
    file_id = os.path.basename(subdir).split('_annotated_images')[0]
    print(file_id)
    pdf_file_path = pdf_files + os.path.basename(subdir).split('_annotated_images')[0] + '.pdf'
    tex_file_path = tex_files + file_id + '_tex_files'
    detected_objects = parse_pdf(pdf_file_path, tex_file_path, 'no', True, False)
    generate_csv_annotations(csv_file_path, file_id, detected_objects)

obtain_txt_train_images_file(csv_file_path, txt_path, '..png_files/test_images/')



