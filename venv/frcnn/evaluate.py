from os import path


class PageInstance:
    def __init__(self, page_objects_list):
        self.x1 = page_objects_list[1]
        self.y1 = page_objects_list[2]
        self.x2 = page_objects_list[3]
        self.y2 = documentObjectList[4]
        self.instance_type = page_objects_list[5]


class Page:
    def __init__(self):
        a = 1


def load_annotations(ground_truth_path, predictions_path):
    print('Loading GT and PREDICTIONS files...')
    with open(ground_truth_path) as ground_truth_file:
        gt_instances = [line.rstrip('\n') for line in ground_truth_file]
    with open(predictions_path) as predictions_file:
        predicted_instances = [line.rstrip('\n') for line in predictions_file]
    print('Files successfully loaded.')

    return gt_instances, predicted_instances


def are_instances_of_the_same_page(gt_line, pred_line):
    gt_pag= obtain_page_from_line(gt_line)
    pred_pag= obtain_page_from_line(pred_line)
    print(gt_pag, pred_pag)

def obtain_page_from_line(line):
    return path.basename(line).split(',')[0].split('_')[1].split('.')[0]

are_instances_of_the_same_page('..png_files/test_images/1901.0235_annotated_images/1901.0235_10.png,169.79600000000005,80.11400000000003,455.88100000000014,257.10200000000003,table', '../png_files/test_images/1901.0235_annotated_images/1901.0235_10.png,114,359,489,375,title')
