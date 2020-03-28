class PageInstance:
    def __init__(self, page_objects_list):
        self.x1 = page_objects_list[1]
        self.y1 = page_objects_list[2]
        self.x2 = page_objects_list[3]
        self.y2 = documentObjectList[4]
        self.instance_type = page_objects_list[5]

class Page:
    def __init__(self):
        a=1

def load_annotations(ground_truth_path, predictions_path):
    print('Loading GT and PREDICTIONS files...')
    with open(ground_truth_path) as ground_truth_file:
        gt_instances = [line.rstrip('\n') for line in ground_truth_file]
    with open(predictions_path) as predictions_file:
        predicted_instances = [line.rstrip('\n') for line in predictions_file]
    print('Files successfully loaded.')

    return gt_instances, predicted_instances



load_annotations('./annotated_test_images.txt', './predicted_test_images.txt')