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
    for i, j in zip(range(len(gt_paper_pages)), range(len(pred_paper_pages))):
        if gt_paper_pages[i].page_number == pred_paper_pages[j].page_number:
            print('ok, evaluate')
        elif gt_paper_pages[i].page_number > pred_paper_pages[j].page_number:
            print('all pred page instances are false positives, iou is 0 for all of them')
        else:
            print('all gt page instances are false negatives, iou is 0 for all of them')


def compute_iou(gt, pred):
    print()


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

