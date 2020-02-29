import pandas as pd
from utils import csv_converter_args

print('Creating annotated_train_images.txt for training task... ')
csv_filename = csv_converter_args().filename
train = pd.read_csv(csv_filename)
train.head()

data = pd.DataFrame()
data['format'] = train['images_name']
# as the images are in train_images folder, add train_images before the image name
for i in range(data.shape[0]):
    dir = str(data['format'][i]).split('_')[0] + '_annotated_images/'
    data['format'][i] = '../png_files/train_images/' + dir + data['format'][i]

# add xmin, ymin, xmax, ymax and class as per the format required
for i in range(data.shape[0]):
    data['format'][i] = data['format'][i] + ',' + str(train['x_min'][i]) + ',' + str(train['y_min'][i]) + ',' + str(train['x_max'][i]) + ',' + str(train['y_max'][i]) + ',' + train['paper_category'][i]

data.to_csv('frcnn/annotated_train_images.txt', header=None, index=None, sep=' ')