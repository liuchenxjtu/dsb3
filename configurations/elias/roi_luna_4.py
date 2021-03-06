from configurations.elias import segnet8
from scripts.elias.blob import blob_dog
from application.luna import LunaDataLoader
from interfaces.data_loader import VALIDATION, TRAINING, TEST, TRAIN, INPUT


# segmentation model
model = segnet8

from inspect import getmembers, isfunction
functions_list = [o for o in getmembers(model) if isfunction(o[1])]
for f in functions_list:
    print f


# the size of the patches, make as big as fits into memory
IMAGE_SIZE = 160
patch_shape = IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE  # in pixels
norm_patch_shape = IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE  # in mms

# plot analysis figures in paths.ANALYSIS_PATH
plot = False
# extract nodules in background thread
multiprocess = True

# the tag for the new data
tag = "luna:"
# put in the pixelspacing tag to be able to make patches
extra_tags=[tag+"pixelspacing"]

# for building the segmentation model, the input tag should be replaced
replace_input_tags = {"luna:3d": tag+"3d"} #{old:new}

# prep before patches
preprocessors = []
# prep on the patches

#################################
# HuNorm happens inside network #
#################################
postpreprocessors = []

data_loader= LunaDataLoader(
    sets=[VALIDATION],
    preprocessors=preprocessors,
    epochs=1,
    multiprocess=False,
    crash_on_exception=True)

batch_size = 1 # only works with 1

# function to call to extract nodules from the fully reconstructed segmentation
def extract_nodules(segmentation):
    """segmentation is a 3D array"""
    rois = blob_dog(segmentation, min_sigma=1, max_sigma=15, threshold=0.1)
    print rois.shape[0]
    if rois.shape[0] > 0:
        rois = rois[:, :3] #ignore diameter
    else: 
        return None
    return rois
