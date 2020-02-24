import csv
import os

def generate_csv_annotations(csv_filename):
    if(not os.path.exists(csv_filename + '.csv')):
        with open(csv_filename + '.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Images_name', 'paper_category', 'x_min', 'x_max', 'y_min', 'y_max'])
            filewriter.writerow(['1', '2', '3', '4', '5', '6'])
    else:
        with open(csv_filename + '.csv', 'a+', newline='') as write_obj:
            filewriter = csv.writer(write_obj)

generate_csv_annotations('prova')