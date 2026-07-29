from tkinter import filedialog, messagebox, Tk
import os
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np

tk_root = Tk()
tk_root.withdraw()

xml_folder = filedialog.askdirectory()

if xml_folder:
    file_list = os.listdir(xml_folder)
    list_data_to_excel = []
    ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}
    column_names=["ID NFe", "CNPJ do Emitente", "Valor Total", "Data e Hora de Emissão", "Data de Emissão"]
    file_name = os.path.abspath(os.path.join(xml_folder, 'tabela_NFe.xlsx'))

    for file in file_list:
        if file.lower().endswith('.xml'):

            file_path = os.path.abspath(os.path.join(xml_folder, file))
            tree = ET.parse(file_path)
            root = tree.getroot()

            infNFe = root.find('.//ns:infNFe', ns)
            NFe_id = infNFe.get('Id').strip() if infNFe is not None else None
            NFe_id = NFe_id.strip('NFe') if NFe_id else None
            emit = root.find('.//ns:emit', ns)
            emit_CNPJ = emit.find('ns:CNPJ', ns) if emit is not None else None
            vNF = root.find('.//ns:vNF', ns)
            dhEmi = root.find('.//ns:dhEmi', ns)
            dEmi = root.find('.//ns:dEmi', ns)

            data_to_excel = {'ID NFe': NFe_id if NFe_id is not None else None, 'CNPJ do Emitente': emit_CNPJ.text if emit_CNPJ is not None else None, 'Valor Total': vNF.text if vNF is not None else None, 'Data e Hora de Emissão': dhEmi.text if dhEmi is not None else None, 'Data de Emissão': dEmi.text if dEmi is not None else None}
            list_data_to_excel.append(data_to_excel)

    if list_data_to_excel:
        new_df = pd.DataFrame(list_data_to_excel, columns=column_names)

        if os.path.isfile(file_name):
            old_df = pd.read_excel(file_name, dtype=str)
            new_df = new_df[~new_df['ID NFe'].isin(old_df['ID NFe'])]
            
            if not new_df.empty:
                try:
                    with pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                        start_row = writer.sheets['Dados'].max_row if 'Dados' in writer.sheets else 0
                        new_df.to_excel(writer, sheet_name='Dados', index=False, header=not start_row, startrow=start_row)
                        messagebox.showinfo("Informação", "Planilha atualizada com sucesso!")   

                except PermissionError:
                    messagebox.showerror("Erro", f'Arquivo "{file_name}" já está aberto e não pode ser acessado. Feche o arquivo e tente novamente.')
                except Exception as e:
                    messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao salvar o arquivo: {e}")
            else:
                 messagebox.showinfo("Informação", "Os dados já estão atualizados.")       
        else:
            try:    
                with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
                    new_df.to_excel(writer, sheet_name='Dados', index=False)   
                    messagebox.showinfo("Informação", "Planilha criada com sucesso!")    

            except PermissionError:
                messagebox.showerror("Erro", f'Arquivo "{file_name}" já está aberto e não pode ser acessado. Feche o arquivo e tente novamente.')
            except Exception as e:
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao salvar o arquivo: {e}")
    else:
        messagebox.showwarning("Informação", "Nenhum arquivo XML encontrado na pasta selecionada.")
tk_root.destroy()
