# teX-annotator for F-RCNN
### A PDF documents annotator, based on lateX files downloaded from arXiv.org, which outputs annotated documents' pages used for a Faster RCNN trainining.

#### 1. Repo contents
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

#### 2. Project structure

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

When the main termines, all is set-up for start with the fcrnn training.

#### 3. Download files from arXiv.org
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

