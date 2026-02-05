import tempfile
import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
from loaders import *

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

@st.cache_data
def le_arquivos_pasta(pasta):
    conteudo = ''
    if os.path.exists(pasta):
        for arquivo in os.listdir(pasta):
            caminho = os.path.join(pasta, arquivo)
            if os.path.isfile(caminho):
                try:
                    if arquivo.lower().endswith('.pdf'):
                        conteudo += carrega_pdf(caminho) + '\n\n'
                    elif arquivo.lower().endswith(('.csv', '.txt', '.pptx', '.docx', '.ppt', '.doc')):
                        conteudo += carrega_docling(caminho) + '\n\n'
                    else:
                         pass
                except Exception as e:
                    print(f"Erro ao ler arquivo {caminho}: {e}")
    return conteudo

KNOWLEDGE_BASE = le_arquivos_pasta('arquivos')

TIPOS_ARQUIVOS_VALIDOS = [
    'Site', 'Youtube', 'Pdf', 'Csv', 'Txt', 'Pptx', 'Docx'
]

MEMORIA = ConversationBufferMemory()

def carrega_arquivos(tipo_arquivo, arquivo):
    documento = ""
    if tipo_arquivo == 'Site':
        documento = carrega_site(arquivo)
    elif tipo_arquivo == 'Youtube':
        documento = carrega_youtube(arquivo)
    elif tipo_arquivo == 'Pdf':
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_pdf(nome_temp)
    elif tipo_arquivo == 'Csv':
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_docling(nome_temp)
    elif tipo_arquivo == 'Txt':
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_docling(nome_temp)
    elif tipo_arquivo == 'Pptx':
        with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_docling(nome_temp)
    elif tipo_arquivo == 'Docx':
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp:
            temp.write(arquivo.read())
            nome_temp = temp.name
        documento = carrega_docling(nome_temp)
    return documento

def carrega_modelo(api_key, tipo_arquivo=None, arquivo=None):
    
    documento = ""
    if arquivo:
        documento = carrega_arquivos(tipo_arquivo, arquivo)

    system_message = f'''Você é um assistente amigável chamado Oráculo.
    Você possui acesso às seguintes informações de base:
    ####
    {KNOWLEDGE_BASE}
    ####
    
    Além disso, você possui acesso às seguintes informações vindas 
    de um documento enviado pelo usuário ({tipo_arquivo if tipo_arquivo else "Nenhum"}): 

    ####
    {documento}
    ####

    Utilize as informações fornecidas para basear as suas respostas.
    Sempre que houver $ na sua saída, substita por S.

    Se a informação do documento for algo como "Just a moment...Enable JavaScript and cookies to continue" 
    sugira ao usuário carregar novamente o Oráculo!'''

    print(system_message)

    template = ChatPromptTemplate.from_messages([
        ('system', system_message),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])
    
    chat = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=api_key)
    chain = template | chat

    st.session_state['chain'] = chain

def pagina_chat():
    st.header('🤖Bem-vindo ao Oráculo', divider=True)

    chain = st.session_state.get('chain')
    if chain is None:
        api_key_input = API_KEY or st.session_state.get('google_api_key')
        if api_key_input:
             carrega_modelo(api_key_input)
             chain = st.session_state.get('chain')
        else:
            st.error('Por favor, adicione a Google API Key na barra lateral para começar.')
            st.stop()

    memoria = st.session_state.get('memoria', MEMORIA)
    for mensagem in memoria.buffer_as_messages:
        chat = st.chat_message(mensagem.type)
        chat.markdown(mensagem.content)

    input_usuario = st.chat_input('Fale com o oráculo')
    if input_usuario:
        chat = st.chat_message('human')
        chat.markdown(input_usuario)

        chat = st.chat_message('ai')
        resposta = chat.write_stream(chain.stream({
            'input': input_usuario, 
            'chat_history': memoria.buffer_as_messages
            }))
        
        memoria.chat_memory.add_user_message(input_usuario)
        memoria.chat_memory.add_ai_message(resposta)
        st.session_state['memoria'] = memoria

def sidebar():
    with st.tabs(['Upload de Arquivos'])[0]:
        tipo_arquivo = st.selectbox('Selecione o tipo de arquivo', TIPOS_ARQUIVOS_VALIDOS)
        arquivo = None
        if tipo_arquivo == 'Site':
            arquivo = st.text_input('Digite a url do site')
        elif tipo_arquivo == 'Youtube':
            arquivo = st.text_input('Digite a url do vídeo')
        elif tipo_arquivo == 'Pdf':
            arquivo = st.file_uploader('Faça o upload do arquivo pdf', type=['.pdf'])
        elif tipo_arquivo == 'Csv':
            arquivo = st.file_uploader('Faça o upload do arquivo csv', type=['.csv'])
        elif tipo_arquivo == 'Txt':
            arquivo = st.file_uploader('Faça o upload do arquivo txt', type=['.txt'])
        elif tipo_arquivo == 'Pptx':
            arquivo = st.file_uploader('Faça o upload do arquivo pptx', type=['.pptx'])
        elif tipo_arquivo == 'Docx':
            arquivo = st.file_uploader('Faça o upload do arquivo docx', type=['.docx'])
            
    # Combined Button for Load/Reload
    if st.button('Carregar Informações', use_container_width=True):
        if API_KEY:
             carrega_modelo(API_KEY, tipo_arquivo, arquivo)
             st.rerun()
        else:
             st.error("API Key não encontrada no ambiente.")

    if st.button('Apagar Histórico de Conversa', use_container_width=True):
        st.session_state['memoria'] = ConversationBufferMemory()
        st.rerun()

def main():
    with st.sidebar:
        sidebar()
    pagina_chat()


if __name__ == '__main__':
    main()