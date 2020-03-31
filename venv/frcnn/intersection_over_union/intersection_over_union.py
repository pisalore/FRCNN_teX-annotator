import numpy as np


# iterate over any papers couple (gt, pred), calculates the iou, precision and recall
def evaluate_test_results(gt_papers_list, pred_papers_list):
    for gt, pred in zip(gt_papers_list, pred_papers_list):
        process_gt_and_pred_papers(gt, pred)


def process_gt_and_pred_papers(gt_paper, pred_paper):
    print('Processing papers... gt: ', gt_paper.paper_name, 'pred: ', pred_paper.paper_name)
    matched_pages, additional_gt_pages, additional_pred_pages = verify_paper_pages_correspondences(gt_paper, pred_paper)
    paper_analytics = PaperAnalytics
    paper_analytics.analyzed_paper_name = gt_paper.paper_name
    paper_analytics.additional_gt_pages = additional_gt_pages
    paper_analytics.additional_pred_pages = additional_pred_pages
    for page in matched_pages:
        matched_gt_page = next(gt_page for gt_page in gt_paper.pages if gt_page.page_number == page)
        matched_pred_page = next(pred_page for pred_page in pred_paper.pages if pred_page.page_number == page)
        print()


def compute_iou(gt, pred):
    print()


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
        self.pages_iou = None
        self.page_precision = None
        self.page_recall = None
        self.overall_iou = None
