![tex-parser](https://github.com/pisalore/FRCNN_teX-annotator/blob/master/images/tex_annotator.png)

# teX-annotator for F-RCNN
### A PDF documents annotator, based on lateX files downloaded from arXiv.org, which outputs annotated documents' pages used for a Faster RCNN trainining.

### 1. Repo contents
In this repo I present a PDF annotator, used to obtains data input for F-RCNN training tasks.
The PDF annotator has the aim to detect:
1. Titles
2. Figures
3. Lists
4. Tables

The teX-annotator uses two type of files: a PDF file and its related lateX source code. It works thanks to the 
informations retrived from two parsing tasks: the first is done with **tex_parser.py**, a python script here 
presented, that analyzes all the *.tex* files linked with its PDF file; then, the second parsing task is done 
using [PDFMIner](https://pypi.org/project/pdfminer/), a very useful tool which collects information from each PDF
line. Once the parsing is finished, the knowledge obtained from those two steps is merged in order to match lateX and PDF
PDF "objects" (titles, figures, tables and lists) and save their **xy coordinates** from *bbox* PDFMiners elements' 
property. So, each object of each page of each PDF file saved in the PDF_files directory is identified and located
thanks to its coordinates: a list is created with all these obejct. A detected object is uniquely represented with
these values memorized into a list:
```python
detected_object = [page, x_min, x_max, y_min, y_max, object_category]
```
* **page**: The object page
* **x_min, y_max**: the bottom left bounding box point
* **x_max, y_max**: the top right bounding box point
* **object_category**: the object category

These are used for ***annotations***: a summary *images_annotations.csv* file, from which is obtained a .txt file
used to indicate to the **Faster RCNN** the training images. The test images are produced during the main program runs.

PDF files and their source files (lateX) have been downloaded from [arXiv.org](https://arxiv.org/); there were not
document layout distinctions in downloading files. 

### 2. Project structure

The project is organized as follows:
```
main.py
```
It's the **main**, and does the following operations:
* It generates as many **.png files** as many pdf pages for each downloaded paper.
* It does **parsing** tasks and **retrievs objects coordinates**.
* It divides train and test images, listed inside *PNG_files* dir, parsing TEX and PDF files, which are stored in
 *PDF_files* and *TEX_files* directories respectively. The **90%** of pdf files will generates **train images**,
  the rest **10%** the **test images** ones.
* It generates ***annotations_images.csv*** and ***annotated_train_images.txt*** files; this last one will be given in input
to the **frcnn**.

The main.py can be launched from shell. There are two optioned commands: 
```
python3 main.py --help
usage: main.py [-h] [--csv_file_path CSV_FILE_PATH]
               [--annotations ANNOTATIONS]

optional arguments:
  -h, --help            show this help message and exit
  --csv_file_path CSV_FILE_PATH
                        Type the .csv file name to convert. By default is:
                        images_annotations. The converter then will generate
                        test_annotations_images.txt and
                        train_annotations_images.txt .
  --annotations ANNOTATIONS
                        Choose if generate annotated images where: red=
                        titles; green= figures; blu= lists; aqua green=
                        tables; yellow= text; typing yes or no.
```
The most of the work is done by **PDF_parser.py**, which calls **tex_parser.py** and optionally the 
**images_annotator.py**. images_annotator.py highlights different objects categories whit different colors:
1. RED -------------> titles
2. GREEN ---------> images
3. BLUE ------------>  lists
4. TURQUOISE ---> tables
5. YELLOW --------> text **NOT USED IN FRCNN**.

When the main finishes, all is set-up for start with the frcnn training.

**NB**: the graphic pages annotations (specifying *--annotations=yes*) could be slow since also text is annotated.

### 3. Download files from arXiv.org
The PDF and teX files are downloaded thanks to **the arXiv_download_script.py**. This script has to be launched before 
the main one because it creates **PDF_files** and **TEX_files** populating them (unless you don't have >10K pdf and related
teX).
**arXiv_download_script.py** can be launched from bash; there are some optional commands:
```
python3 arXiv_download_script.py --h
usage: arXiv_download_script.py [-h] [--year YEAR] [--month MONTH]
                                [--counter COUNTER] [--max_items MAX_ITEMS]

optional arguments:
  -h, --help            show this help message and exit
  --year YEAR           Choose the year from which you want to start
                        downloading papers from arXIv. Default 20.
  --month MONTH         Choose the month, once you have choseh the year, from
                        which you want to start downloading papers from arXIv.
                        Default 1(janaury)
  --counter COUNTER     Choose the starting file counter. With 0 you will
                        download all files from the year and the month
                        specified.Default 0.
  --max_items MAX_ITEMS
                        Chose how many files you will download

```
These commands take into accounts how papers are saved on arXiv.org.

### 4. F-RCNN 
The annotated images serve as F-RCNN input data; the goal of this project is to test how much correctly the net can
detects **titles, figures, lists and tables**. For this task I've chosen the F-RCNN net; further informations about it 
are available on [R-CNN, Fast R-CNN, Faster R-CNN, YOLO — Object Detection Algorithms](https://towardsdatascience.com/r-cnn-fast-r-cnn-faster-r-cnn-yolo-object-detection-algorithms-36d53571365e).
I've cloned the repo from this git repo [keras-frcnn](https://github.com/kbardool/keras-frcnn) and the I've followed
this [guide](https://www.analyticsvidhya.com/blog/2018/11/implementation-faster-r-cnn-python-object-detection/) for implementation.
Start with training is very easy: open the shell, go to /DDM_Project/venv/frcnn/ and start!

```
cd frcnn
python3 train_frcnn.py -o simple -p annotated_train_images.txt
```

This command will start training which will generate an h5 model, that is the input for test:
```
python3 test_frcnn.py -p ../png_files/test_images/
```
The **test** procedure will outputs the **annotated test images** basing on the training task results.


### 5. Test evaluation 

Test evaluation is available. After test task, a **.txt** file will be generated with the result images: **predicted_test_images.txt**.
This file contains all the details about all the instances detected during the test (obviously concerning the test set). 
Furthermore, it's important to generate a similar file which constitutes the Ground Truth. Such a file has to be created
after the FRCNN test phase, running the **test_images_annotator.py** script.
```
python3 test_images_annotator.py
```
This script will generate the **annotated_test_images.txt** and the **parse_error_test_files.txt**, which will contains the paper name
that have been badly elaborated (parsing errors); this file is very important because, before the test evaluation, it is crucial
to remove all the lines which refers to the erroneous papers in the **annotated_test_images.txt**: such an operation insures
an unique correspondence between the GT and the predictions (**annotated_test_images.txt** and **predicted_test_images.txt**).

Once you have done this operation, you can evaluate your FRCNN predictions simply running the **evaluate.py** script:
NB: It is very important that you sort the **predicted_test_images.txt** and the **annotated_test_images.txt**
running this command:
```
sort -u -o <file_to_sort> <file_where_output_sort_operation>
```
Then, run:
 ```
python3 evaluate.py
```

This script will generate:
- a log with all the GT papers and another with all the PREDICTION papers; these logs file 
could be useful if correspondence problems occur.
- a **test_results.txt** file which contains all the information about the test evaluation of all the single papers.
This file is so constructed: 
    - PRED and GT different pages lists
    - Precision
    - Recall
    - True Positives, False Positives, False Negatives
    - F1 score
    
All these statistics are evaluated varying a threshold value used in the **Intersection Over Union**
(IoU) algorithm used for predicted papers instances classification. The used thresholds are:
[0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80].

An F1-PRECISION-RECALL plot it is shown after the computation, giving an idea of the test accuracy.

    

### 6. Requirements
The dipendencies required for this project are listed inside **requirements.txt**; you should simply open a shell and
use ***pip3*** running:

```
pip3 install -r requirements.txt
```
For this project I used Python **3.7**; I recommend to use PyCharm.

### 7: Numbers, examples, results
I would like to share with you some numbers:
* **10.200** pdf files processed (papers and various scientific articles) downloaded from arXIv.
    * 9 180 for training set
    * 1 020 for test set
* **204 658** relative papers source files downloaded from arXiv
* **187 485** png files generated, one image for one paper page
* **466452** instances (titles, images, lists and tables) found and analyzed with frcnn.


### 8. References
This project has been inspired by **PubLayNet**, a project where PDF taken from the PubMed Central dataset
(over 360 thousands of articles!) are annotated with theirs relative XML files. PubLayNet paper is
available [here](https://arxiv.org/pdf/1908.07836.pdf).

Here an example of the PubLayNet paper annotated using tex-annotator!

![publaynet-ann](https://github.com/pisalore/FRCNN_teX-annotator/blob/master/images/publaynet_ann.jpg)

