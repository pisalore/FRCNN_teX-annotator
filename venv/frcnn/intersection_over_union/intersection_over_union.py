# evaluate_test_results calculates iou for each instance, precision, recall; it also collects for each all different
# pages (pages which belong to gt not in pred and viceversa). All progress are saved in a txt file. Precision and recall
# results are also plotted.
import numpy as np
import os

log_path = './logs/test_results.txt'


# iterate over any papers couple (gt, pred), calculates the iou, precision and recall
def evaluate_test_results(gt_papers_list, pred_papers_list):
    # In pages_analyzes all paper analytics will be saved
    papers_analyzes = []
    if os.path.exists(log_path):
        os.remove(log_path)
    results_test_log_file = open(log_path, 'a+')
    results_test_log_file.write('TEST RESULTS LOG \n')
    results_test_log_file.close()
    for gt, pred in zip(gt_papers_list, pred_papers_list):
        paper_analytics = process_gt_and_pred_papers(gt, pred)
        papers_analyzes.append(paper_analytics)

    return papers_analyzes


def process_gt_and_pred_papers(gt_paper, pred_paper):
    print('Processing papers... gt: ', gt_paper.paper_name, 'pred: ', pred_paper.paper_name)
    # In pages_analyzes all examined paper pages analytics will be saved
    pages_analyzes = []
    results_test_log_file = open(log_path, 'a+')
    results_test_log_file.write('ANALYZED PAPER: ' + gt_paper.paper_name + '\n')
    results_test_log_file.close()
    # Loading pages matched between gt and pred papers and different pages
    matched_pages, additional_gt_pages, additional_pred_pages = verify_paper_pages_correspondences(gt_paper, pred_paper)
    # instantiate the paper analytics obj where save all the information collected for a paper in test analysis
    paper_analytics = PaperAnalytics
    # name of analyzed paper
    paper_analytics.analyzed_paper_name = gt_paper.paper_name
    # gt pages which are not in pred paper
    paper_analytics.additional_gt_pages = additional_gt_pages
    # pred pages which are not in gt paper
    paper_analytics.additional_pred_pages = additional_pred_pages
    # call compute_iou in order to calculate iou for each matched page; in page_analyzes of paper analytics I save all
    # the statistics for that page for each instance
    for page in matched_pages:
        matched_gt_page = next(gt_page for gt_page in gt_paper.pages if gt_page.page_number == page)
        matched_pred_page = next(pred_page for pred_page in pred_paper.pages if pred_page.page_number == page)
        # here the page analysis is computed
        page_analytics = process_page_analysis(matched_gt_page, matched_pred_page)
        pages_analyzes.append(page_analytics)

    paper_analytics.pages_analyzes = pages_analyzes
    paper_analytics.overall_precision = np.mean([analyzed_page.page_precision for analyzed_page
                                                 in paper_analytics.pages_analyzes])
    paper_analytics.overall_recall = np.mean([analyzed_page.page_recall for analyzed_page
                                              in paper_analytics.pages_analyzes])
    return paper_analytics


def process_page_analysis(gt_page, pred_page):
    # Initialization of true positives, false positives and false negatives in order to calculate precision and recall;
    # page instance analytics object initialization for the specific gt instance
    tp, fp, fn = 0, 0, 0
    page_analytics = PageAnalytics()
    for gt_instance in gt_page.page_instances:
        page_instance_analytics = PageInstanceAnalytics()
        iou = 0
        best_iou_pred_instance = None
        # I iterate over all the prediction instances, calculating the iou only for the ones which are of the same
        # gt_instance type; I save the instance which realizes the max iou
        for pred_instance in pred_page.page_instances:
            if pred_instance.instance_type == gt_instance.instance_type:
                tmp_iou = intersection_over_union(gt_instance.x1, gt_instance.y1,
                                                  gt_instance.x2, gt_instance.y2, pred_instance.x1,
                                                  pred_instance.y1, pred_instance.x2,
                                                  pred_instance.y2)
                if tmp_iou > iou:
                    iou, best_iou_pred_instance = tmp_iou, pred_instance
        if iou > 0.4 and best_iou_pred_instance:
            tp += 1
            page_instance_analytics.page_instance = best_iou_pred_instance
            page_instance_analytics.iou = iou
            page_analytics.matched_instances.append(page_instance_analytics)
        else:
            fn += 1
    # Here I calculate the false positives, iterating for each pred instance over the gt instances; if not satisfying
    # iou, the a fp is found
    for pred_instance in pred_page.page_instances:
        iou = 0
        for gt_instance in gt_page.page_instances:
            if gt_instance.instance_type == pred_instance.instance_type:
                tmp_iou = intersection_over_union(gt_instance.x1, gt_instance.y1,
                                                  gt_instance.x2, gt_instance.y2, pred_instance.x1,
                                                  pred_instance.y1, pred_instance.x2,
                                                  pred_instance.y2)
                if tmp_iou > iou:
                    iou = tmp_iou

        if iou < 0.4:
            fp += 1

    page_analytics.page_precision = float(tp / (tp + fp))
    page_analytics.page_recall = float(tp / (tp + fn))

    return page_analytics


def intersection_over_union(gt_x1, gt_y1, gt_x2, gt_y2, pred_x1, pred_y1, pred_x2, pred_y2):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(gt_x1, pred_x1)
    yA = max(gt_y1, pred_y1)
    xB = min(gt_x2, pred_x2)
    yB = min(gt_y2, pred_y2)
    # compute the area of intersection rectangle
    inter_area = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    # compute the area of both the prediction and ground-truth
    # rectangles
    box_gt_area = (gt_x2 - gt_x1 + 1) * (gt_y2 - gt_y1 + 1)
    box_pred_area = (pred_x2 - pred_x1 + 1) * (pred_y2 - pred_y1 + 1)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the intersection area
    iou = inter_area / float(box_gt_area + box_pred_area - inter_area)
    # return the intersection over union value
    return iou


# return three lists: match pages, paper1 pages not in paper2 pages, paper2 pages not in paper1 pages
def verify_paper_pages_correspondences(paper1, paper2):
    paper1_number_of_pages = [page.page_number for page in paper1.pages]
    paper2_number_of_pages = [page.page_number for page in paper2.pages]
    paper1_pages_not_in_paper2 = [value for value in paper1_number_of_pages if value not in paper2_number_of_pages]
    paper2_pages_not_in_paper1 = [value for value in paper2_number_of_pages if value not in paper1_number_of_pages]
    matched_pages = [value for value in paper1_number_of_pages if value in paper2_number_of_pages]
    return matched_pages, paper1_pages_not_in_paper2, paper2_pages_not_in_paper1


class PaperAnalytics:
    def __init__(self):
        self.analyzed_paper_name = None
        self.pages_analyzes = None
        self.overall_precision = None
        self.overall_recall = None
        self.overall_iou = None
        self.additional_gt_pages = None
        self.additional_pred_pages = None


class PageAnalytics:
    def __init__(self):
        self.matched_instances = None
        self.page_precision = None
        self.page_recall = None
        self.overall_iou = None


class PageInstanceAnalytics:
    def __init__(self, ):
        self.iou = 0
        self.page_instance = None
