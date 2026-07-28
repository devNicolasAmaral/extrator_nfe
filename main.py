from tkinter import filedialog
import os
import xml.etree.ElementTree as ET

xml_folder = filedialog.askdirectory()

if xml_folder:
    file_list = os.listdir(xml_folder)

    for file in file_list:
        if file.lower().endswith('.xml'):
            file_path = os.path.abspath(os.path.join(xml_folder, file))
            tree = ET.parse(file_path)
            root = tree.getroot()
            print(root.tag)
