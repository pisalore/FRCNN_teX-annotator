import pdf_parser
import glob
import os

PDF_FILES = 'pdf_files/'
TEX_FILES = 'tex_files/'

def main():
    for pdf_file_path in glob.glob(os.path.join(PDF_FILES, '*.pdf')):
        file_id = str(os.path.basename(pdf_file_path).split('.pdf')[0])
        tex_file_path = TEX_FILES + file_id + '_tex_files'
        if(os.path.exists(tex_file_path)):
            print('\nParsing ' + pdf_file_path +'...')
            pdf_parser.parse_pdf(pdf_file_path, tex_file_path)

if __name__ == "__main__":
    main()
