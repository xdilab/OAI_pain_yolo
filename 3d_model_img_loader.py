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
hrmoradi = True  # TODO:  if Hamidreza Moradi = True  <<<<<<<<<<<  Hunter = False

# lets us know number of images in that file
dirpath = "/Users/huntersylvester/Desktop/UMMC/Research/Moradi/sample_knee_mri_localization/9009067_10287112_R_Progressed"
if hrmoradi: dirpath = "C:\\Users\\hrmor\OneDrive - University of Mississippi Medical Center\\05_Pycharm\\OAI_pain\\sample_knee_mri_localization\\9009067_10287112_R_Progressed\\"

num_layers = len(fnmatch.filter(os.listdir(dirpath), '*.jpg'))
print("num_layers for a patient: ", num_layers)

# This will walk through files in directory and rename jpgs in correct order
# os.chdir(dirpath)
directory = "/Users/huntersylvester/Desktop/UMMC/Research/Moradi/sample_knee_mri_localization"
if hrmoradi: directory = "C:\\Users\\hrmor\OneDrive - University of Mississippi Medical Center\\05_Pycharm\\OAI_pain\\sample_knee_mri_localization\\"

print("len directories: ", len(list(glob.iglob(f"{directory}/*"))))
for filename in glob.iglob(f"{directory}/*"):
    print(filename)
    i = 0
    x = os.path.join(directory,
                     filename)  # TODO: why join? for me the addresses are the same for x and filename (if different on your system disregard)
    print(x)
    os.chdir(x)
    for file in natsorted(glob.glob("*.jpg")):  # TODO: good library!
        i += 1
        filename = "layer" + str(i) + ".jpg"
        print(f"{i} + {filename}")
        os.rename(file,
                  filename)  # TODO: there is no need to rename them! keep original names so later we can refer, just sort and keep in numpy
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
# TODO: (3, 11, 384, 384) is better, first dimention patients, second layers, 3/4 th images, then another numpy of size 3 will have labels! [progressed, not progressed, progressed]
# TODO: which as of now might be easier to read from folder names