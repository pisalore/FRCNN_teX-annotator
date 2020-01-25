import os
import tempfile
from PyPDF2.pdf import PdfFileReader
from pdf2image import convert_from_path

filename = 'pdf_files/2001.05970.pdf'
reader = PdfFileReader(open('pdf_files/2001.05970.pdf',  mode="rb"))
page_number = reader.getNumPages()
with tempfile.TemporaryDirectory() as path:
    images_from_path = convert_from_path(filename, output_folder=path, last_page=page_number, first_page=0)

save_dir = 'jpeg_files'

i = 0
for page in images_from_path:
    base_filename = os.path.splitext(os.path.basename(filename))[0] + str(i) +'.jpg'
    page.save(os.path.join(save_dir, base_filename), 'JPEG')
    i += 1