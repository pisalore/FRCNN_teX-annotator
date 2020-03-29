from os import path

# return paper page from line
def obtain_page_from_line(line):
    return path.basename(line).split(',')[0].split('_')[1].split('.')[0]


# verifies if two instances are from the same paper page
def are_instances_of_the_same_page(gt_line, pred_line):
    gt_pag = obtain_page_from_line(gt_line)
    pred_pag = obtain_page_from_line(pred_line)
    if gt_pag == pred_pag:
        return True


# return paper name from line
def obtain_paper_from_line(line):
    return path.basename(line).split(',')[0].split('_')[0]


# add Pages objects to a Paper list of Pages from all instances (lines) of a paper
def add_pages(all_pages_instances):
    list_of_pages = []
    page_instances = []
    current_page = None
    for line_instance in all_pages_instances:
        tmp_page = obtain_page_from_line(line_instance)
        if not current_page:
            current_page = tmp_page
        if current_page == tmp_page:
            page_instances.append(line_instance)
        else:
            page = Page(page_instances)
            list_of_pages.append(page)
            page_instances = [line_instance]
            current_page = tmp_page

    return list_of_pages


def add_instances_to_page(page_instances):
    # TODO: from a line of page_instances generate a PageInstance object
    print()


class Paper:
    def __init__(self, all_paper_instances):
        self.paper_name = obtain_paper_from_line(all_paper_instances[0])
        self.all_paper_instances = all_paper_instances
        self.pages = add_pages(self.all_paper_instances)


class Page:
    def __init__(self, all_page_instances):
        self.page_number = obtain_page_from_line(all_page_instances[0])
        self.all_page_instances = add_instances_to_page(self.all_page_instances)


class PageInstance:
    def __init__(self, page_objects_list):
        self.x1 = page_objects_list[1]
        self.y1 = page_objects_list[2]
        self.x2 = page_objects_list[3]
        self.y2 = documentObjectList[4]
        self.instance_type = page_objects_list[5]


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
        if current_paper == tmp_paper:
            paper.append(instance_line)
        else:
            list_of_papers.append(paper)
            log_file.write(str(current_paper) + '\n')
            current_paper = tmp_paper
            paper = [instance_line]

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


gt, pred = load_annotations('./annotated_test_images.txt', './predicted_test_images.txt')
a = retrieve_papers_from_instances(gt, 'ground_truth')
b = retrieve_papers_from_instances(pred, 'predictions')

prova = Paper(a[0])
print(prova)
