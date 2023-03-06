import os
import xml.etree.ElementTree as ET
import shutil


# Define the label map
# label_map = {"KneeJointArea_Lat": 0}
label_map = {"SagKneeJointArea": 0}

path = ".\\knee_mri_localization\\"
subFoldered_path = ".\\knee_mri_localization_3sub\\"
onRoot_path = ".\\knee_mri_localization_allinRoot\\"

if True:         # TODO: copies all files to corressponding folder ::  image -> images, xml label -> labels_xml, created yolo compatible .txt -> labels # 3 sub folder per patient #

    for subdir in os.listdir(path):

        from_path = os.path.join(path, subdir)
        to_path = os.path.join(subFoldered_path, subdir)
        os.makedirs(to_path, exist_ok=True)

        # create """images""" folder
        images_folder = os.path.join(to_path, "images")
        os.makedirs(images_folder, exist_ok=True)
        # move images files
        for file in os.listdir(from_path):
            if file.endswith(".jpg"):
                file_path = os.path.join(from_path, file)
                shutil.copy(file_path, images_folder)

        # create """labels_xml""" folder
        xml_labels_folder = os.path.join(to_path, "labels_xml")
        os.makedirs(xml_labels_folder, exist_ok=True)
        # move xml files
        for file in os.listdir(from_path):
            if file.endswith(".xml"):
                file_path = os.path.join(from_path, file)
                shutil.move(file_path, xml_labels_folder)

        # create """labels""" folder <<>>> yolo compatible
        txt_labels_folder = os.path.join(to_path, "labels")
        os.makedirs(txt_labels_folder, exist_ok=True)
        # Loop over all the label files
        for filename in os.listdir(xml_labels_folder):
            # Load the XML file
            tree = ET.parse(os.path.join(xml_labels_folder, filename))
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
                # print(obj.find("name").text)
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
            label_filename = os.path.join(txt_labels_folder, os.path.splitext(filename)[0] + ".txt")
            with open(label_filename, "w") as f:
                f.write("\n".join(labels))


if True:         # TODO: copy all the files in sib folder to the root of a folder

    images_folder = os.path.join(onRoot_path, "images")
    os.makedirs(images_folder, exist_ok=True)
    txt_labels_folder = os.path.join(onRoot_path, "labels")
    os.makedirs(txt_labels_folder, exist_ok=True)

    for root, dirs, files in os.walk(subFoldered_path):
        for file in files:
            src_file = os.path.join(root, file)
            parent = str(src_file).split("\\")[-3]
            print(root," | " ,file, " | " ,parent)
            if '.xml' in file:
                continue
            if '.jpg' in file:
                dest_file = os.path.join(images_folder, parent + "_" + file)
                shutil.copy(src_file, dest_file)
            if '.txt' in file:
                dest_file = os.path.join(txt_labels_folder, parent + "_" + file)
                shutil.copy(src_file, dest_file)
