#tes per scaricare files da arXIv
import urllib.request

pdf_files_path = 'pdf_files/'
tex_files_path = 'tex_files/'

pdf_download_url = 'https://arxiv.org/pdf/'
source_download_url = 'https://arxiv.org/e-print/'
year = 10
month = 1
file_counter = 0
file_identifier = ''

while year <=20:
    if len(str(month)) == 1:
        file_identifier = '0' + str(month) + str(year)
    file_counter_digits = len(str(file_counter))
    if file_counter_digits == 1:
        file_identifier += '.000' + str(file_counter)
    elif file_counter_digits == 2:
        file_identifier += '.00' + str(file_counter)
    elif file_counter_digits == 3:
        file_identifier += '.0' + str(file_counter)
    elif file_counter_digits == 4:
        file_identifier += '.'+str(file_counter)





    # urllib.request.urlretrieve("https://arxiv.org/pdf/1001.0003", pdf_files_path + "file.pdf")