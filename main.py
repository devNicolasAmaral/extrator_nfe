from tkinter import filedialog, messagebox, Tk
import os
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
from datetime import datetime

def get_path():
        return filedialog.askdirectory()

def extract_xml_data(xml_folder):
    files_list = os.listdir(xml_folder)
    raw_data_list = []
    files_error = []
    ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

    for file in files_list:
        if file.lower().endswith('.xml'):
            try:
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
                raw_data_dict = {'ID NFe': NFe_id if NFe_id is not None else None, 'CNPJ do Emitente': emit_CNPJ.text if emit_CNPJ is not None else None, 'Valor Total': vNF.text if vNF is not None else None, 'Data e Hora de Emissão': dhEmi.text if dhEmi is not None else None, 'Data de Emissão': dEmi.text if dEmi is not None else None}

                raw_data_list.append(raw_data_dict)
                
            except ET.ParseError as e:
                files_error.append(file)
                continue

    return raw_data_list, files_error 

def create_log_file(xml_folder, file_error):
    log_file = os.path.abspath(os.path.join(xml_folder, f'log_file_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.txt'))

    if file_error:
            with open(log_file, 'w') as f:
                for e in file_error:
                    print(e)
                    f.write(f'{e}\n')

    return log_file

def filter_dataframe(raw_data_list, excel_file):
    column_names=["ID NFe", "CNPJ do Emitente", "Valor Total", "Data e Hora de Emissão", "Data de Emissão"]
    
    if not raw_data_list:
        return pd.DataFrame(raw_data_list, columns=column_names)

    new_df = pd.DataFrame(raw_data_list, columns=column_names)

    if os.path.isfile(excel_file):
        old_df = pd.read_excel(excel_file, dtype=str)
        new_df = new_df[~new_df['ID NFe'].isin(old_df['ID NFe'])]

    return new_df

def save_to_excel(new_df, excel_file):
    if new_df.empty:
        return 'no changes' 

    try:
        if os.path.isfile(excel_file):       
            with pd.ExcelWriter(excel_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                start_row = writer.sheets['Dados'].max_row if 'Dados' in writer.sheets else 0
                new_df.to_excel(writer, sheet_name='Dados', index=False, header=not start_row, startrow=start_row)
                return 'spreadsheet updated' 
        else:  
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                new_df.to_excel(writer, sheet_name='Dados', index=False)   
                return 'spreadsheet created'

    except PermissionError:
        return 'permission error'
    except Exception as e:
        return f'generic error', e 
    
def main():
    tk_root = Tk()
    tk_root.withdraw()

    xml_folder = get_path()

    if xml_folder:
        excel_file = os.path.abspath(os.path.join(xml_folder, f'Tabela_NFe.xlsx'))
        full_data_list = extract_xml_data(xml_folder)  
        raw_data_list = full_data_list[0]  
        file_error = full_data_list[1]
        log_file = create_log_file(xml_folder, file_error)
        new_df = filter_dataframe(raw_data_list, excel_file)
        message_text = save_to_excel(new_df, excel_file)

        match message_text[0]:
            case 'spreadsheet updated': 
                messagebox.showinfo("Informação", "Planilha atualizada com sucesso!")   
            case 'permission error':
                messagebox.showerror("Erro", f'Arquivo "{excel_file}" já está aberto e não pode ser acessado. Feche o arquivo e tente novamente.')
            case 'no changes' if not raw_data_list:
                messagebox.showwarning("Informação", "Nenhum arquivo XML encontrado na pasta selecionada.")
            case 'no changes': 
                messagebox.showinfo("Informação", "Os dados já estão atualizados.")  
            case 'spreadsheet created':     
                messagebox.showinfo("Informação", "Planilha criada com sucesso!")    
            case _: 
                messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao salvar o arquivo: {message_text[1]}")
            
        if file_error:
            messagebox.showwarning("Atenção", f"Alguns arquivos foram ignorados por estarem corrompidos ou vazios. \nVeja mais detalhes em: {log_file}")

    tk_root.destroy()

if __name__ == "__main__":
    main()