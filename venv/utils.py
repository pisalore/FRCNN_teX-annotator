import argparse

def download_script_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', default='20', help=' Choose the year from which you want to start'
                                                       ' downloading papers from arXIv. Default 20.')
    parser.add_argument('--month', default='1', help=' Choose the month, once you have choseh the year, from which you want to start'
                                                     ' downloading papers from arXIv. Default 1(janaury)')
    parser.add_argument('--counter', default='0', help='Choose the starting file counter. With 0 you will download all files'
                                                       ' from the year and the month specified.Default 0.')
    parser.add_argument('--max_items', default='1', help='Chose how many files you will download')

    args = parser.parse_args()
    return args

def main_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv_file_path', default='images_annotations.csv',
                        help='Type the .csv file name to convert. By default is: images_annotations. '
                             'The converter then will generate test_annotations_images.txt and train_annotations_images.txt .')
    parser.add_argument('--annotations', default='no', help='Choose if generate annotated images where:'
                                                            ' red= titles; green= figures; blu= lists; aqua green= tables; yellow= text;'
                                                            ' typing yes or no.')
    args = parser.parse_args()
    return args
