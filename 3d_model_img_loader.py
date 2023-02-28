from PIL import Image
import numpy as np

image_list = []

for i in range(num_layers):  #
    filename = "layer" + str(i) + ".jpg"
    im = Image.open(filename)
    image_list.append(im)
    
image_array = np.array([np.array(im) for im in image_list])

