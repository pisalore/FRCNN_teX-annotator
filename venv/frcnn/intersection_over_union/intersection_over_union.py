import numpy as np


# iterate over any papers couple (gt, pred), calculates the iou, precision and recall
def evaluate_test_results(gt_papers_list, pred_papers_list):
    for gt, pred in zip(gt_papers_list, pred_papers_list):
        process_gt_and_pred_papers(gt, pred)


def process_gt_and_pred_papers(gt_paper, pred_paper):
    print('Processing papers... gt: ', gt_paper.paper_name, 'pred: ', pred_paper.paper_name)
    paper_analytics = PaperAnalytics
    gt_paper_pages = gt_paper.pages
    pred_paper_pages = pred_paper.pages
    paper_analytics.analyzed_paper_name = gt_paper.paper_name
    j = 0
    for gt_page in gt_paper_pages:
        for pred_page in pred_paper_pages:
            if gt_page.page_number == pred_page.page_number:
                print('ok, evaluate')


def compute_iou(gt, pred):
    print()


# return a list of three lists: match pages, paper1 pages not in paper2 pages, paper2 pages not in paper1 pages
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


class PageAnalytics:
    def __init__(self):
        self.pages_iou = None
        self.page_precision = None
        self.page_recall = None
        self.overall_iou = None
