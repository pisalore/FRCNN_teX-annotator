#tes per scaricare files da arXIv
import urllib.request
import os
import tarfile

pdf_files_path = 'pdf_files/'
test = 'test_dw_pdf/'
tex_files_path = 'tex_files/'

pdf_download_url = 'https://arxiv.org/pdf/'
source_download_url = 'https://arxiv.org/e-print/'
year = 10
month = 2
file_counter = 0
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

    print('Downloading ' + file_identifier + '.pdf and its source files from arXiv...')
    downloaded_pdf_file_path = test + file_identifier +".pdf"
    downloaded_tar_file_path = test + file_identifier + ".tar"
    try:
        urllib.request.urlretrieve(pdf_download_url + file_identifier, downloaded_pdf_file_path)
        if os.path.exists(downloaded_pdf_file_path):
            urllib.request.urlretrieve(source_download_url + file_identifier, downloaded_tar_file_path)
            extract_tar_dir_path = test + file_identifier + '_tex_files'
            os.mkdir(extract_tar_dir_path)
            tar = tarfile.open(downloaded_tar_file_path)
            tar.extractall(path=extract_tar_dir_path)
            tar.close()

        print('Files succesfully downloaded. \n')
    except:
        print('PDF or Source files for ' + file_identifier + 'not found. Download the next file.')
        file_counter = 0
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        if os.path.exists(downloaded_pdf_file_path):
            os.remove(downloaded_pdf_file_path)


# 2002.4425