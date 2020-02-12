#tes per scaricare files da arXIv
import urllib.request

pdf_files_path = 'pdf_files/'
test = 'test_dw_pdf/'
tex_files_path = 'tex_files/'

pdf_download_url = 'https://arxiv.org/pdf/'
source_download_url = 'https://arxiv.org/e-print/'
year = 10
month = 12
file_counter = 6044
file_identifier = ''

while year <=20:
    file_counter += 1
    if len(str(month)) == 1:
        file_identifier =  str(year) + '0' +str(month)
    else:
        file_identifier = str(year) + str(month)
    file_counter_digits = len(str(file_counter))
    if file_counter_digits == 1:
        file_identifier += '.000' + str(file_counter)
    elif file_counter_digits == 2:
        file_identifier += '.00' + str(file_counter)
    elif file_counter_digits == 3:
        file_identifier += '.0' + str(file_counter)
    elif file_counter_digits == 4:
        file_identifier += '.' + str(file_counter)

    print('Downloading ' + file_identifier + '.pdf ...')

    try:
        urllib.request.urlretrieve(pdf_download_url + file_identifier, test + file_identifier +".pdf")
    except:
        file_counter = 0
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1


# 1001.5471