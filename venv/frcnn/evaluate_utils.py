import argparse


def evaluate_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pred_path', default='./predicted_test_images.txt',
                        help='Type the .txt file name where test images predictions are stored. By default is:'
                             ' ./predicted_test_images.txt. ')
    parser.add_argument('--gt_path', default='./annotated_test_images',
                        help='Type the .txt file name where test images annotations (the ground truth) are stored.'
                             '  By default is: ./annotated_test_images.txt. ')
    args = parser.parse_args()
    return args
