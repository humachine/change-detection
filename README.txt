- Copy this folder to any location on disk
- Open config.py and make sure IMG_DIR points to the directory which has all the input images
- Input Image pairs have to be of the format stringa.png, stringb.png; i.e *a.png & *b.png

- DriverNew.py contains the driver function that runs the entire program.
- DriverNew first calls Setup.py which creates the necessary Output directories. All directories can be changed in config.py
- ALL vital constants can be changed in config.py (There are none to very-minimal number of hard-coded values in the entire codebase)