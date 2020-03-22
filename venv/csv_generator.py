import csv
import os

def generate_csv_annotations(csv_filename, file_id, detected_objects):
    if(not os.path.exists(csv_filename)):
        with open(csv_filename, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['images_name', 'paper_category', 'x_min', 'x_max', 'y_min', 'y_max'])

            for object in detected_objects:
                image_name = file_id + '_' + str(object[0]) + '.png'
                filewriter.writerow([image_name, object[-1], object[1], object[3], object[4], object[2]])
    else:
        with open(csv_filename, 'a+', newline='') as write_obj:
            filewriter = csv.writer(write_obj)
            if not detected_objects:
                filewriter.writerow([file_id, 'not valid'])
            for object in detected_objects:
                image_name = file_id + '_' + str(object[0]) + '.png'
                filewriter.writerow([image_name, object[-1], object[1], object[3], object[4], object[2]])