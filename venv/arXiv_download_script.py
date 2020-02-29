import urllib.request
import urllib.error
import os
import tarfile
from utils import download_script_parse_args
import datetime

def check_next_paper(file_identifier):
    p1 = file_identifier.split('.')[0]
    p2 = file_identifier.split('.')[1]
    p2 = int(p2) + 1
    try:
        urllib.request.urlopen('https://arxiv.org/pdf/' + str(p1) + '.' + str(p2))
    except:
        return False
    return True

args = download_script_parse_args()

pdf_files_path = 'pdf_files/'
tex_files_path = 'tex_files/'

if not os.path.exists(pdf_files_path):
    os.mkdir(pdf_files_path)
if not os.path.exists(tex_files_path):
    os.mkdir(tex_files_path)

pdf_download_url = 'https://arxiv.org/pdf/'
source_download_url = 'https://arxiv.org/e-print/'
current_date = datetime.datetime.now()
current_year = str(current_date.year)[-2:]
year = int(args.year)
month = int(args.month)
file_counter = int(args.counter)
max_items = int(args.max_items)
file_identifier = ''
num_downloaded_files = 1
if year <= int(str(current_date.year)[-2:]):
    while num_downloaded_files <= max_items:
        file_counter += 1
        num_downloaded_files += 1
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
        elif file_counter_digits == 4 or file_counter_digits == 5:
            file_identifier += '.' + str(file_counter)

        print('Downloading ' + file_identifier + '.pdf and its source files from arXiv...')
        downloaded_pdf_file_path = pdf_files_path + file_identifier +".pdf"
        extract_tar_dir_path = tex_files_path + file_identifier + '_tex_files'
        downloaded_source_file_path = extract_tar_dir_path + file_identifier + ".tar"
        try:
            urllib.request.urlretrieve(pdf_download_url + file_identifier, downloaded_pdf_file_path)
            if os.path.exists(downloaded_pdf_file_path):
                os.mkdir(extract_tar_dir_path)
                urllib.request.urlretrieve(source_download_url + file_identifier, downloaded_source_file_path)
                downloaded_source_file = tarfile.open(downloaded_source_file_path)
                downloaded_source_file.extractall(path=extract_tar_dir_path)
                downloaded_source_file.close()
                if os.path.exists(downloaded_source_file_path):
                    os.remove(downloaded_source_file_path)
                print('Files succesfully downloaded. \n')
        except urllib.error.HTTPError :
            print(urllib.error.HTTPError.code, '. The requested paper does not exist or there are some problems with the internet connection.')
            if os.path.exists(downloaded_source_file_path):
                os.remove(downloaded_source_file_path)
            if os.path.exists(extract_tar_dir_path):
                os.rmdir(extract_tar_dir_path)
            if os.path.exists(downloaded_pdf_file_path):
                os.remove(downloaded_pdf_file_path)
            print('PDF or Source files for ' + file_identifier + ' not found. Download the next file.\n')
            if not check_next_paper(file_identifier):
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
            if os.path.exists(downloaded_pdf_file_path):
                os.remove(downloaded_pdf_file_path)
        except tarfile.ReadError:
            print('Cannot read the tar file. Remove all its references (PDF and dir).\n')
            if os.path.exists(downloaded_source_file_path):
                os.remove(downloaded_source_file_path)
            if os.path.exists(extract_tar_dir_path):
                os.rmdir(extract_tar_dir_path)
            if os.path.exists(downloaded_pdf_file_path):
                os.remove(downloaded_pdf_file_path)
else:
    print('You cannot download papers from future!')
    exit(0)