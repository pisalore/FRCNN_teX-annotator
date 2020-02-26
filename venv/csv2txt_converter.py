import pandas as pd
train = pd.read_csv('train.csv')
train.head()
data = pd.DataFrame()
data['format'] = train['images_name']

# as the images are in train_images folder, add train_images before the image name
for i in range(data.shape[0]):
    data['format'][i] = 'png_files/1901.0401_annotated_images/' + data['format'][i]

# add xmin, ymin, xmax, ymax and class as per the format required
for i in range(data.shape[0]):
    data['format'][i] = data['format'][i] + ',' + str(train['x_min'][i]) + ',' + str(train['y_min'][i]) + ',' + str(train['x_max'][i]) + ',' + str(train['y_max'][i]) + ',' + train['paper_category'][i]

data.to_csv('annotate.txt', header=None, index=None, sep=' ')