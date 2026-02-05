# Oraculo

Oraculo é uma aplicação interativa desenvolvida com **Streamlit** que permite carregar diversos tipos de documentos e fontes de dados (como PDFs, CSVs, sites e vídeos do YouTube) para criar uma base de conhecimento. A aplicação utiliza modelos de Inteligência Artificial (via **LangChain** e **Google Generative AI**) para responder perguntas com base no conteúdo carregado.

## Funcionalidades

-   **Carregamento de Documentos**: Suporte para diversos formatos de arquivo e fontes externas:
    -   Arquivos locais: PDF, CSV, TXT, DOCX, PPTX.
    -   Fontes Web: URLs de sites e vídeos do YouTube.
-   **Base de Conhecimento**: A aplicação lê automaticamente arquivos presentes na pasta `arquivos/` ao iniciar.
-   **Interface Interativa**: Chatbot integrado para interagir com o conteúdo processado.
-   **Processamento de Texto**: Utiliza `Docling` e `LangChain` para extração e processamento eficiente de texto.

## Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina.

## Instalação

1.  Clone este repositório.
2.  Crie um ambiente virtual (recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\\Scripts\\activate
    ```
3.  Instale as dependências listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## Configuração

O projeto utiliza variáveis de ambiente para configuração de chaves de API.

1.  Crie um arquivo `.env` na raiz do projeto.
2.  Adicione sua chave de API do Google (Gemini) no arquivo `.env`:
    ```env
    GOOGLE_API_KEY=sua_chave_aqui
    ```

## Como executar

Para iniciar a aplicação, utilize o comando do Streamlit:

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador padrão.

## Estrutura do Projeto

-   `app.py`: Arquivo principal da aplicação Streamlit.
-   `loaders.py`: Contém as funções para carregar e processar diferentes tipos de documentos (PDF, Web, YouTube, etc.).
-   `arquivos/`: Pasta onde arquivos de conhecimento podem ser colocados para leitura automática.
-   `requirements.txt`: Lista de dependências do projeto. 
