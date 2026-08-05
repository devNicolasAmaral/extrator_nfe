# Extrator NFe

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

Aplicação em Python para automatizar a extração em massa de dados de Notas Fiscais XML, eliminando o processo manual de leitura, organização e geração de planilhas.

---

## Funcionalidades

- Leitura em lote de arquivos XML
- Extração automática dos dados fiscais
- Tratamento e organização das informações
- Geração de planilha Excel
- Interface gráfica para seleção da pasta de processamento

---

## Stack

| Camada | Tecnologia |
| :--- | :--- |
| Linguagem | Python |
| Processamento | Pandas |
| XML | xml.etree |
| Excel | Openpyxl |
| Interface | Tkinter |
| Distribuição | PyInstaller |

---

## Executando

### Usuário final

1. Baixe a versão mais recente em **Releases**.

2. Execute o programa.

3. Selecione a pasta contendo os XMLs.

4. Aguarde a geração automática da planilha.

---

### Desenvolvedor

```bash
git clone https://github.com/devNicolasAmaral/extrator_nfe

cd extrator_nfe

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Estrutura do processamento

O projeto segue o fluxo ETL:

1. Extract

Leitura dos XMLs.

2. Transform

Extração e tratamento das informações.

3. Load

Geração automática da planilha Excel.
