from config import *
def mkdirifnotexists(DIR_NAME):
    if not os.path.exists(DIR_NAME):
        os.makedirs(DIR_NAME)
        

def setup():
    mkdirifnotexists(OUT_DIR)
    os.chdir(OUT_DIR)
    mkdirifnotexists(RES_DIR)
    mkdirifnotexists(stringify.STRINGIFY_DIR)    
    mkdirifnotexists(thinning.SKEL_IMG_DIR)    
    mkdirifnotexists(removelines.FILL_IMG_DIR)
    mkdirifnotexists(segmentation.OUT_DIR)    
    mkdirifnotexists(segmentation.DEBUG_DIR)    
    mkdirifnotexists(removelines.SAVE_DIR)
    mkdirifnotexists(labeltosegment.OUT_DIR)
    mkdirifnotexists(properties.OUT_DIR)
