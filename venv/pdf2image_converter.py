import os
import tempfile
from PyPDF2.pdf import PdfFileReader
from pdf2image import convert_from_path

filename = 'pdf_files/2001.05994.pdf'
print("Converting " + filename + " from pdf to PNG...")
reader = PdfFileReader(open(filename,  mode="rb"))
page_number = reader.getNumPages()
with tempfile.TemporaryDirectory() as path:
    images_from_path = convert_from_path(filename, dpi=72, output_folder=path, last_page=page_number, first_page=0)

save_dir = 'png_files'

i = 0
for page in images_from_path:
    base_filename = os.path.splitext(os.path.basename(filename))[0] + '_' + str(i) +'.png'
    page.save(os.path.join(save_dir, base_filename), 'PNG')
    i += 1