hrmoradi = True  # TODO:  if Hamidreza Moradi = True  <<<<<<<<<<<  Hunter = False

import fnmatch
import glob
import os
from natsort import natsorted
from PIL import Image
import numpy as np

# Empty list to store numpy arrays
image_list = []
y = []

# lets us know number of images in that file
dirpath = "/Users/huntersylvester/Desktop/UMMC/Research/Moradi/sample_knee_mri_localization/9009067_10287112_R_Progressed"
if hrmoradi: dirpath = "C:\\Users\\hrmor\OneDrive - University of Mississippi Medical Center\\05_Pycharm\\OAI_pain\\sample_knee_mri_localization\\9009067_10287112_R_Progressed\\"
num_layers = len(fnmatch.filter(os.listdir(dirpath), '*.jpg'))
print(num_layers)

# This will walk through files in directory and rename jpgs in correct order
directory = "/Users/huntersylvester/Desktop/UMMC/Research/Moradi/sample_knee_mri_localization"
if hrmoradi: directory = "C:\\Users\\hrmor\OneDrive - University of Mississippi Medical Center\\05_Pycharm\\OAI_pain\\sample_knee_mri_localization\\"
for filename in glob.iglob(f"{directory}/*"):
    i = 0
    os.chdir(filename)
    x = filename.find('_NotProgressed')  # Will give -1 if phrase not in string
    if x > 0:
        y.append(0)  # non progressed 0
    else:
        y.append(1)  # progressed 1
    image_patient = []
    for file in natsorted(glob.glob("*.jpg")):
        i += 1
        im = Image.open(file)
        image_patient.append(np.array(im))
        if i != num_layers:
            pass
        else:
            print(f"number of layers: {i}")
    image_list.append(np.array(image_patient))

image_list = np.array(image_list)

print(len(image_list), len(image_list[0]), len(image_list[0][0]))
print(type(image_list), type(image_list[0]), type(image_list[0][0]))
print(y)
