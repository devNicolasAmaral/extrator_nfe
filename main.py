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

            ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

            print(f"{file}:")
            for elem in root.findall('.//ns:emit', ns):

                child = elem.find('ns:CNPJ', ns)

                if child is not None:
                    print(f"CNPJ: {child.text}")

            elem = root.find('.//ns:vNF', ns)
            if elem is not None:
                print(f"Valor Total: {elem.text}")

            elem = root.find('.//ns:dhEmi', ns)
            if elem is not None:
                print(f"Data e Hora de Emissão: {elem.text}")

            elem = root.find('.//ns:dEmi', ns)
            if elem is not None:
                print(f"Data de Emissão: {elem.text}")
            print()
