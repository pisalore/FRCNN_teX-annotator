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

The scripts projects are organized as follows:
```
main.py
```
It's the **main**, and do the following operations:
* It divides train and test images, parsing TEX and PDF files, which are stored in *PDF_files* and *TEX_files*
 directories respectively. The **90%** of pdf files will generates **train images**, the rest **10%** the **test images** ones.
* It does **parsing** tasks and **retrievs objects coordinates**.
* It generates the ***annotations_images.csv** and ***annotated_train_images.txt***; this one will be given in input
to the **frcnn**.