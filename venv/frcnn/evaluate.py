import os
from intersection_over_union.evaluate_utils import evaluate_args
from intersection_over_union.intersection_over_union import evaluate_test_results, verify_paper_pages_correspondences, \
    thresholds, class_num, log_path
import numpy as np
import matplotlib.pyplot as plt


# return the specified information from a line in order to correctly initialize an instance object
def obtain_instance_value_from_line(line, pos):
    return line.split(',')[pos]


# return paper page from line
def obtain_page_from_line(line):
    return os.path.basename(line).split(',')[0].split('_')[1].split('.')[0]


# return paper name from line
def obtain_paper_from_line(line):
    return os.path.basename(line).split(',')[0].split('_')[0]


# verifies if two instances are from the same paper page
def are_instances_of_the_same_page(gt_line, pred_line):
    gt_pag = obtain_page_from_line(gt_line)
    pred_pag = obtain_page_from_line(pred_line)
    if gt_pag == pred_pag:
        return True


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
    list_of_instances = []
    for instance_line in page_instances:
        page_instance = PageInstance(instance_line)
        list_of_instances.append(page_instance)
    return list_of_instances


class Paper:
    def __init__(self, all_paper_instances):
        self.paper_name = obtain_paper_from_line(all_paper_instances[0])
        self.all_paper_instances = all_paper_instances
        self.pages = add_pages(self.all_paper_instances)
        self.pages.sort(key=lambda x: x.page_number)


class Page:
    def __init__(self, all_page_instances):
        self.page_number = int(obtain_page_from_line(all_page_instances[0]))
        self.page_instances = add_instances_to_page(all_page_instances)
        self.paper = obtain_paper_from_line(all_page_instances[0])


class PageInstance:
    def __init__(self, page_instance):
        self.filepath = obtain_instance_value_from_line(page_instance, 0)
        self.x1 = float(obtain_instance_value_from_line(page_instance, 1))
        self.y1 = float(obtain_instance_value_from_line(page_instance, 2))
        self.x2 = float(obtain_instance_value_from_line(page_instance, 3))
        self.y2 = float(obtain_instance_value_from_line(page_instance, 4))
        self.instance_type = obtain_instance_value_from_line(page_instance, 5)


# return a list of papers (instances is a list of strings; each string item is a line)
def retrieve_papers_from_instances(instances, annotations_type):
    log_path = './logs/' + annotations_type + '_papers.txt'
    if os.path.exists(log_path):
        os.remove(log_path)
    log_file = open(log_path, 'a+')
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


def precision_recall_plot(precision, recall, f1):
    fig, ax = plt.subplots()
    x = thresholds
    ax.plot(x, precision, label='precision')
    ax.plot(x, recall, label='recall')
    ax.plot(x, f1, label='f1 score')
    ax.set_xlabel('thresholds')  # Add an x-label to the axes.
    ax.set_ylabel('Percentage')  # Add a y-label to the axes.
    ax.set_title("Precision-Recall-F1 Plot")  # Add a title to the axes.
    ax.legend()


def main():
    args = evaluate_args()
    pred_path = args.pred_path
    gt_path = args.gt_path
    gt_papers = []
    predictions_papers = []
    papers_counter = 0
    gt_annotations, pred_annotations = load_annotations(gt_path, pred_path)
    gt_papers_annotations = retrieve_papers_from_instances(gt_annotations, 'ground_truth')
    pred_papers_annotations = retrieve_papers_from_instances(pred_annotations, 'predictions')
    print('Preparations of gt test papers objects...')
    for gt in gt_papers_annotations:
        gt_paper = Paper(gt)
        print('Created paper object: ', gt_paper.paper_name)
        gt_papers.append(gt_paper)
        papers_counter += 1
        print('Processed ' + str(papers_counter) + ' gt papers')
    print('Preparations of predictions test papers objects...')
    papers_counter = 0
    for pred in pred_papers_annotations:
        pred_paper = Paper(pred)
        print('Created paper object: ', pred_paper.paper_name)
        predictions_papers.append(pred_paper)
        papers_counter += 1
        print('Processed ' + str(papers_counter) + ' predictions papers')
    print('All papers generated.')
    # here I've correctly collected all my Papers object; now, I've to pass them to the IoU calculator.
    # The lists of papers are predictions_papers and gt_papers
    analytics = evaluate_test_results(gt_papers, predictions_papers)
    print('Analysis successfully terminated.')
    # Here I calculate the precision, recall and f1 score means considering all the papers for all the threshold, which
    # are 15 number; changing the thresholds list obviously is possible to obtain different analysis
    f1 = [np.mean([paper.f1_score[i] for paper
                   in analytics]) * 100 for i in range(len(thresholds))]
    precision = [np.mean([paper.overall_precision[i] for paper
                          in analytics]) * 100 for i in range(len(thresholds))]
    recall = [np.mean([paper.overall_recall[i] for paper
                       in analytics]) * 100 for i in range(len(thresholds))]
    all_gt_papers_instances_per_class = np.zeros((len(thresholds), class_num))
    all_pred_papers_instances_per_class = np.zeros((len(thresholds), class_num))
    for paper in analytics:
        all_gt_papers_instances_per_class = np.sum([all_gt_papers_instances_per_class,
                                                   paper.all_gt_paper_instances_per_class], axis=0)
        all_pred_papers_instances_per_class = np.sum([all_pred_papers_instances_per_class,
                                                     paper.all_pred_paper_instances_per_class], axis=0)
    all_ratios_between_gt_and_pred_per_class_by_threshold = all_pred_papers_instances_per_class / all_gt_papers_instances_per_class * 100
    print(all_ratios_between_gt_and_pred_per_class_by_threshold)
    results_test_log_file = open(log_path, 'a+')

    results_test_log_file.write('\nClasses instances divided by threshold: GT annotations.\n'
                                'Titles, Figures, Tables, Lists \n'
                                + str(all_gt_papers_instances_per_class))
    results_test_log_file.write('\nClasses instances divided by threshold: PREDICTIONS.\n'
                                'Titles, Figures, Tables, Lists \n'
                                + str(all_pred_papers_instances_per_class))
    results_test_log_file.write('\nClasses instances divided by threshold: RATIOS.\n'
                                'Titles, Figures, Tables, Lists \n'
                                + str(all_ratios_between_gt_and_pred_per_class_by_threshold))
    results_test_log_file.close()
    precision_recall_plot(precision, recall, f1)
    plt.show()


if __name__ == "__main__":
    main()
