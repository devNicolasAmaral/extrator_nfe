# Extrator NFe 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

> Software focado em automação ETL que elimina o trabalho manual, operando com extração em massa de dados de Notas Fiscais em XML e devolução tabelada em planilhas Excel.

## ⚙️ Arquitetura e Decisões Técnicas

* **Padrão ETL (Extract, Transform, Load):** A arquitetura foi modularizada para isolar cada etapa do processamento. A extração das tags é feita diretamente dos arquivos XML, seguida pela filtragem e transformação dos dados necessários em memória, e finalizada com a carga e estruturação automatizada do relatório final em `.xlsx`.
* **Mitigação de Falhas (Early Returns):** O fluxo de execução implementa *early returns* para validação prévia de estado. Isso previne o travamento da aplicação ao lidar com diretórios vazios, permissões negadas ou arquivos corrompidos, garantindo resiliência na operação em lote.
* **Isolamento de Responsabilidade (SRP):** O motor de processamento de dados foi estritamente desacoplado da interface gráfica (Tkinter). Essa decisão garante que a regra de negócio se mantenha agnóstica à UI, permitindo que, no futuro, o extrator possa ser executado de forma invisível (headless) em servidores ou integrado a uma API sem refatoração profunda.

## 🛠️ Stack Tecnológica

* **Linguagem:** Python
* **Processamento de Dados:** Pandas, Openpyxl, xml.etree
* **Interface Gráfica:** Tkinter
* **Build/Distribuição:** PyInstaller

## 🚀 Como Executar

### Para o Usuário Final

1. Acesse a página de [Releases](https://github.com/devNicolasAmaral/extrator_nfe/releases/latest) do projeto.
2. Faça o download do arquivo executável (`main.exe` ou `Extrator-NFe.exe`).
3. Execute o software. Na interface gráfica, selecione a pasta onde estão armazenados os arquivos XML das Notas Fiscais.
4. Aguarde o processamento. O sistema gerará automaticamente uma planilha chamada `Tabela_NFe.xlsx` dentro do mesmo diretório informado, contendo todos os dados tabulados.

### Para Desenvolvedores (Build Local)

Caso deseje inspecionar o código, modificar regras de negócio ou compilar o próprio binário, siga os passos abaixo:

```bash
# Clone o repositório
git clone [https://github.com/devNicolasAmaral/extrator_nfe](https://github.com/devNicolasAmaral/extrator_nfe)

# Acesse o diretório do projeto
cd extrator_nfe

# Crie o ambiente virtual na pasta atual
python -m venv .venv

# Ative o ambiente virtual (Windows)
.venv\Scripts\activate

# Instale as dependências mapeadas
pip install -r requirements.txt
```