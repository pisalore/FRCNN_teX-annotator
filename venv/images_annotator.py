import numpy as np
import cv2
import matplotlib.pyplot as plt


def annotate_img(filename, coordinates, first_page, color):
    current_page = first_page
    save_directory = filename + '_annotated_images/'
    file_path = 'png_files/' + save_directory + filename + '_'
    img = cv2.imread(file_path + str(current_page) + '.png')
    for i in range(len(coordinates)):
        page = coordinates[i][0]
        if current_page != page:
            current_page = page
            img = cv2.imread(file_path + str(page) + '.png')
        start_point = []
        start_point.append(int(coordinates[i][1]))
        start_point.append(int(coordinates[i][2]))
        end_point = []
        end_point.append(int(coordinates[i][3]))
        end_point.append(int(coordinates[i][4]))
        start_point = tuple(start_point)
        end_point = tuple(end_point)
        img = cv2.rectangle(img, start_point, end_point, color, 3)
        path = file_path + str(current_page) + '.png'
        cv2.imwrite(path, img)


    # cv2.imshow('image', img)
    # cv2.waitKey(0)
