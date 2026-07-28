from tkinter import filedialog
import os


xml_folder = filedialog.askdirectory()

if xml_folder != '':
    file_list = os.listdir(xml_folder)

    for file in file_list:
        if file.lower().endswith('.xml'):
            print(os.path.abspath(os.path.join(xml_folder, file)))
else:
    print("Nenhuma pasta selecionada.")



