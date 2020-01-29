import numpy as np
import cv2
import matplotlib.pyplot as plt


def annotate_img(coordinates, first_page):
    current_page = first_page
    img = cv2.imread('png_files/2001.05970_' + str(current_page) + '.png', 0)
    for i in range(len(coordinates)):
        page = coordinates[i][0]
        if current_page != page:
            current_page = page
            img = cv2.imread('png_files/2001.05970_' + str(page) + '.png', 0)
        start_point = []
        start_point.append(int(coordinates[i][1]))
        start_point.append(int(coordinates[i][2]))
        end_point = []
        end_point.append(int(coordinates[i][3]))
        end_point.append(int(coordinates[i][4]))
        start_point = tuple(start_point)
        end_point = tuple(end_point)
        img = cv2.rectangle(img, start_point, end_point, (0, 255, 0), 3)
        path = 'png_files/2001.05970_' + str(current_page) + '.png'
        cv2.imwrite(path, img)


    # cv2.imshow('image', img)
    # cv2.waitKey(0)
