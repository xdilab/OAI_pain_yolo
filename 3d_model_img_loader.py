# Moradi's original code/idea
# from PIL import Image
# import numpy as np

# image_list = []

# for i in range(num_layers):  #
#     filename = "layer" + str(i) + ".jpg"
#     im = Image.open(filename)
#     image_list.append(im)
    
# image_array = np.array([np.array(im) for im in image_list])


import fnmatch
import glob
import os
from natsort import natsorted
from PIL import Image
import numpy as np

# Empty list to store numpy arrays
image_list = []

# lets us know number of images in that file
dirpath = "/Users/huntersylvester/Desktop/UMMC/Research/Moradi/sample_knee_mri_localization/9009067_10287112_R_Progressed"
num_layers = len(fnmatch.filter(os.listdir(dirpath), '*.jpg'))
print(num_layers)

# This will walk through files in directory and rename jpgs in correct order
# os.chdir(dirpath)
directory = "/Users/huntersylvester/Desktop/UMMC/Research/Moradi/sample_knee_mri_localization"
for filename in glob.iglob(f"{directory}/*"):
    i = 0
    x = os.path.join(directory, filename)
    os.chdir(x)
    for file in natsorted(glob.glob("*.jpg")):
        i += 1
        filename = "layer" + str(i) + ".jpg"
        print(f"{i} + {filename}")
        os.rename(file, filename)
        im = Image.open(filename)
        image_list.append(im)
        if i != num_layers:
            pass
        else:
            print(f"number of layers: {i}")

image_array = np.array([np.array(im) for im in image_list])

print(image_array)

print(len(image_array))

print(image_array.shape)
