import os
import tempfile
from PyPDF2.pdf import PdfFileReader
from pdf2image import convert_from_path

def generate_images(path, save_dir_name, is_train):
    if not os.path.exists('png_files/'):
        os.mkdir('png_files/')
    train_images = 'train_images/'
    test_images = 'test_images/'
    if is_train:
        save_directory_path = 'png_files/'+ train_images + save_dir_name + '_annotated_images'
    else:
        save_directory_path = 'png_files/' + test_images + save_dir_name + '_annotated_images'

    if not os.path.exists(save_directory_path):
        os.makedirs(save_directory_path)
    filename = path
    print("Converting " + filename + " from pdf to PNG...")
    reader = PdfFileReader(open(filename, mode="rb"))
    try:
        page_number = reader.getNumPages()
    except:
        page_number = reader.getNumPages()
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(filename, dpi=72, output_folder=path, last_page=page_number, first_page=0)
    i = 0
    for page in images_from_path:
        base_filename = os.path.splitext(os.path.basename(filename))[0] + '_' + str(i + 1) + '.png'
        page.save(os.path.join(save_directory_path, base_filename), 'PNG')
        i += 1

    print('PDF file successfully converted.')
