import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', default='20', help=' Choose the year from which you want to start'
                                                       ' downloading papers from arXIv.')
    parser.add_argument('--month', default='1', help=' Choose the month, once you have choseh the year, from which you want to start'
                                                     ' downloading papers from arXIv.')
    parser.add_argument('--counter', default='0', help='Choose the starting file counter. With 0 you will download all files'
                                                       'form the year and the month specified.')

    args = parser.parse_args()
    return args
