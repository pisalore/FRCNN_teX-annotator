import pandas as pd


def obtain_txt_train_images_file(csv_file_path, txt_path, files_path):
    print('Creating annotations in txt format.. \n')
    print('Reading csv file...')
    train = pd.read_csv(csv_file_path)
    print('Reading completed.')
    train.head()

    data = pd.DataFrame()
    data['format'] = train['images_name']
    # as the images are in train_images folder, add train_images before the image name
    for i in range(data.shape[0]):
        print('Loaded row n°: ', i)
        dir = str(data['format'][i]).split('_')[0] + '_annotated_images/'
        data['format'][i] = files_path + dir + data['format'][i]

    # add xmin, ymin, xmax, ymax and class as per the format required
    for i in range(data.shape[0]):
        print('Saved row n°: ', i)
        data['format'][i] = data['format'][i] + ',' + str(train['x_min'][i]) + ',' + str(train['y_min'][i]) + ',' + str(train['x_max'][i]) + ',' + str(train['y_max'][i]) + ',' + train['paper_category'][i]

    data.to_csv(txt_path, header=None, index=None, sep=' ')

#obtain_txt_train_images_file('images_annotations.csv')