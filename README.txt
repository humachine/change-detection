INSTRUCTIONS:
- Copy this folder to any location on disk
- Open config.py and make sure IMG_DIR points to the directory which has all the input images
- Input Image pairs have to be of the format stringa.png, stringb.png; i.e *a.png & *b.png

- DriverNew.py contains the driver function that runs the entire program.
- DriverNew first calls Setup.py which creates the necessary Output directories. All directories can be changed in config.py
- ALL vital constants can be changed in config.py (There are none to very-minimal number of hard-coded values in the entire codebase)

- The Results are Saved in %OUT_DIR% / %RES_DIR% from config.py

 
REQUIREMENTS:
- Python 2.7 (64-bit)

Packages Needed : 
- Numpy
- Scipy
- Opencv-python (Cv2, cv)
- Python-Tesseract (https://code.google.com/p/python-tesseract/ | EXE file attached)
- Pickle
- PIL (Python Imaging Library)
- Itertools, itemgetter, time, collections and some inbuilt Python packages as well


The entire code was developed and tested on a machine with the following specifications:
Processor : Intel Core i5-2500 CPU @ 3.30GHz
Memory : 16GB DDR3 RAM
System :  64-bit Windows 7

The entire code (although not tested on other environments) is expected to work on similar systems with 8GB RAM and above and on several Linux distributions too. 