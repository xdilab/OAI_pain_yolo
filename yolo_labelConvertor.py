import os
import xml.etree.ElementTree as ET

LABELS_PATH = "./sample_one/labels_xml/"
IMAGES_PATH = "./sample_one/images/"
OUTPUT_PATH = "./sample_one/labels/"

# Define the label map
label_map = {"KneeJointArea_Lat": 0}

# Loop over all the label files
for filename in os.listdir(LABELS_PATH):
    # Load the XML file
    tree = ET.parse(os.path.join(LABELS_PATH, filename))
    root = tree.getroot()

    # Get the image dimensions
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    # Create a list to store the YOLO v7 format labels
    labels = []

    # Loop over all the objects in the image
    for obj in root.findall("object"):
        label = obj.find("name").text
        label_id = label_map[label]

        bbox = obj.find("bndbox")
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        # Convert the coordinates to YOLO v7 format
        x_center = (xmin + xmax) / 2.0 / width
        y_center = (ymin + ymax) / 2.0 / height
        w = (xmax - xmin) / width
        h = (ymax - ymin) / height

        # Add the label to the list
        labels.append(f"{label_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

    # Save the labels to a text file
    # image_name = os.path.splitext(filename)[0] + ".jpg"
    label_filename = os.path.join(OUTPUT_PATH, os.path.splitext(filename)[0] + ".txt")
    with open(label_filename, "w") as f:
        f.write("\n".join(labels))

    # Copy the image file to the output folder