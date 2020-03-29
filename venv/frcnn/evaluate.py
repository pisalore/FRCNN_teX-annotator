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


class Paper:
    def __init__(self):
        b = 2


# return a list of papers (instances is a list of strings; each string item is a line)
def retrieve_papers_from_instances(instances, type):
    log_file = open('./logs/' + type + '.txt', 'a+')
    list_of_papers = []
    paper = []
    current_paper = None
    for instance_line in instances:
        tmp_paper = obtain_paper_from_line(instance_line)
        if not current_paper:
            current_paper = tmp_paper
            paper.append(instance_line)
        elif current_paper == tmp_paper:
            paper.append(instance_line)
        else:
            list_of_papers.append(paper)
            log_file.write(str(current_paper) + '\n')
            current_paper = tmp_paper
            paper = []
            paper.append(instance_line)

    return list_of_papers


# load gt and predicted annotations
def load_annotations(ground_truth_path, predictions_path):
    print('Loading GT and PREDICTIONS files...')
    with open(ground_truth_path) as ground_truth_file:
        gt_instances = [line.rstrip('\n') for line in ground_truth_file]
    with open(predictions_path) as predictions_file:
        predicted_instances = [line.rstrip('\n') for line in predictions_file]
    print('Files successfully loaded.')
    return gt_instances, predicted_instances


# verifies if two instances are from the same paper page
def are_instances_of_the_same_page(gt_line, pred_line):
    gt_pag = obtain_page_from_line(gt_line)
    pred_pag = obtain_page_from_line(pred_line)
    if gt_pag == pred_pag: return True


# return paper page from line
def obtain_page_from_line(line):
    return path.basename(line).split(',')[0].split('_')[1].split('.')[0]


# return paper name from line
def obtain_paper_from_line(line):
    return path.basename(line).split(',')[0].split('_')[0]


gt, pred = load_annotations('./annotated_test_images.txt', './predicted_test_images.txt')
a = retrieve_papers_from_instances(gt, 'ground_truth')
b = retrieve_papers_from_instances(pred, 'predictions')
