from tkinter import filedialog, messagebox, Tk
import os
import xml.etree.ElementTree as ET
import pandas as pd

tk_root = Tk()
tk_root.withdraw()

xml_folder = filedialog.askdirectory()

if xml_folder:
    file_list = os.listdir(xml_folder)
    list_data_to_excel = []
    ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    column_names=["CNPJ do Emitente", "Valor Total", "Data e Hora de Emissão", "Data de Emissão"]
    file_name = os.path.abspath(os.path.join(xml_folder, 'tabela_NFe.xlsx'))

    for file in file_list:
        if file.lower().endswith('.xml'):

            file_path = os.path.abspath(os.path.join(xml_folder, file))
            tree = ET.parse(file_path)
            root = tree.getroot()

            emit = root.find('.//ns:emit', ns)
            emit_CNPJ = emit.find('ns:CNPJ', ns) if emit is not None else None
            vNF = root.find('.//ns:vNF', ns)
            dhEmi = root.find('.//ns:dhEmi', ns)
            dEmi = root.find('.//ns:dEmi', ns)

            data_to_excel = {'CNPJ do Emitente': emit_CNPJ.text if emit_CNPJ is not None else None, 'Valor Total': vNF.text if vNF is not None else None, 'Data e Hora de Emissão': dhEmi.text if dhEmi is not None else None, 'Data de Emissão': dEmi.text if dEmi is not None else None}
            list_data_to_excel.append(data_to_excel)

    if list_data_to_excel:
        try:
            if os.path.isfile(file_name):
                df_new = pd.DataFrame(list_data_to_excel, columns=column_names)
                with pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                    start_row = writer.sheets['Dados'].max_row if 'Dados' in writer.sheets else 0
                    df_new.to_excel(writer, sheet_name='Dados', index=False, header=not start_row, startrow=start_row)
            else:
                with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
                    df = pd.DataFrame(list_data_to_excel, columns=column_names)
                    df.to_excel(writer, sheet_name='Dados', index=False)    
        except PermissionError:
            messagebox.showerror("Erro", f'Arquivo "{file_name}" já está aberto e não pode ser acessado. Feche o arquivo e tente novamente.')
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao salvar o arquivo: {e}")
    else:
        messagebox.showinfo("Informação", "Nenhum arquivo XML encontrado na pasta selecionada.")
tk_root.destroy()
