import numpy as np


def evaluate_test_results(gt_papers_list, pred_papers_list):
    for gt, pred in zip(gt_papers_list, pred_papers_list):
        process_gt_and_pred_papers(gt, pred)


def process_gt_and_pred_papers(gt_paper, pred_paer):
    print('Processing papers... gt: ', gt_paper.paper_name, 'pred: ', pred_paer.paper_name)


def compute_iou(gt, pred):
    print()


class PaperAnalytics:
    def __init__(self):
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

