import tempfile
import streamlit as st
import os
from langchain.memory import ConversationBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Configuração da página
st.set_page_config(page_title="Oráculo AI", page_icon="✨", layout="wide")

# --- UI ENHANCEMENTS (CSS) ---
st.markdown("""
    <style>
    /* Fundo gradiente profundo */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #1e1f20 0%, #131314 100%);
        color: #e3e3e3;
    }

    /* Estilização da Sidebar (Glassmorphism) */
    section[data-testid="stSidebar"] {
        background-color: rgba(30, 31, 32, 0.7) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Logo e Títulos */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #4285f4, #9b72cb, #d96570);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    /* Balões de Chat Estilizados */
    .stChatMessage {
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: rgba(255, 255, 255, 0.03) !important;
    }

    /* Input de Chat com contorno brilhante */
    .stChatInputContainer {
        border-radius: 30px !important;
        border: 1px solid rgba(66, 133, 244, 0.3) !important;
        background: rgba(30, 31, 32, 0.9) !important;
        padding: 5px !important;
    }

    /* Efeito Aurora nos Botões */
    .stButton button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(90deg, #1e1f20, #2d2e30);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        border-color: #4285f4;
        box-shadow: 0 0 15px rgba(66, 133, 244, 0.4);
        transform: translateY(-2px);
    }

    /* Widget de upload */
    .stFileUploader section {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Esconder cabeçalho padrão do Streamlit */
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# --- LÓGICA DE NEGÓCIO ---

@st.cache_data
def le_arquivos_pasta(pasta):
    # (Sua lógica original de leitura de arquivos...)
    return "Conteúdo base da pasta arquivos..." # Placeholder para exemplo

KNOWLEDGE_BASE = le_arquivos_pasta('arquivos')
# Mapeamento para interface simplificada
TIPOS_ARQUIVOS_VALIDOS_UI = ["PDF", "TXT", "URL Site", "YouTube"]

def carrega_modelo(api_key, tipo_arquivo=None, arquivo=None):
    # Simulação para o exemplo (Mantenha sua lógica original aqui)
    template = ChatPromptTemplate.from_messages([
        ('system', f"Você é o Oráculo. Base: {KNOWLEDGE_BASE}"),
        ('placeholder', '{chat_history}'),
        ('user', '{input}')
    ])
    # Usando gemini-2.0-flash-exp para garantir estabilidade
    chat = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=api_key)
    st.session_state['chain'] = template | chat

# --- INIT SESSION STATE ---
if "memoria" not in st.session_state:
    st.session_state.memoria = ConversationBufferMemory()

# --- SIDEBAR ---
def sidebar():
    st.markdown("<h1 style='color: white; font-size: 1.5rem;'>✨ Oráculo</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("📁 Upload de Contexto")
    tipo = st.selectbox("Fonte de dados", TIPOS_ARQUIVOS_VALIDOS_UI)
    
    arquivo = None
    if tipo in ["PDF", "TXT"]:
        arquivo = st.file_uploader(f"Arraste seu {tipo}")
    else:
        # Simplificação: tratar inputs de texto (Urls)
        arquivo = st.text_input(f"Link do {tipo}")
        
    if st.button("🪄 Atualizar Base"):
        if API_KEY:
            with st.spinner("Sincronizando oráculo..."):
                carrega_modelo(API_KEY, tipo, arquivo)
                st.toast("Conhecimento atualizado com sucesso!", icon="✅")
        else:
            st.error("API Key não configurada.")

    st.markdown("<br>"*5, unsafe_allow_html=True)
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.memoria = ConversationBufferMemory()
        st.rerun()

# --- MAIN PAGE ---
def pagina_chat():
    st.markdown("<h1 class='main-title'>Oráculo ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8E918F; margin-left: 5px;'>Sua inteligência avançada de documentos.</p>", unsafe_allow_html=True)

    # Verifica se o modelo está carregado
    chain = st.session_state.get('chain')
    if chain is None:
        if API_KEY:
             carrega_modelo(API_KEY)
             chain = st.session_state.get('chain')
        else:
            st.warning('⚠️ Adicione a API Key no .env para começar.')
            st.stop()
            
    # Container para as mensagens
    chat_container = st.container()

    with chat_container:
        for mensagem in st.session_state.memoria.buffer_as_messages:
            role = "user" if mensagem.type == "human" else "assistant"
            avatar = "👤" if role == "user" else "https://img.icons8.com/fluency/48/sparkling.png"
            with st.chat_message(role, avatar=avatar):
                st.markdown(mensagem.content)

    # Input fixo
    if prompt := st.chat_input("Fale com o Oráculo..."):
        # Mensagem do usuário
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Resposta com efeito de streaming
        with st.chat_message("assistant", avatar="https://img.icons8.com/fluency/48/sparkling.png"):
            try:
                resposta = st.write_stream(chain.stream({
                    'input': prompt, 
                    'chat_history': st.session_state.memoria.buffer_as_messages
                }))
                
                st.session_state.memoria.chat_memory.add_user_message(prompt)
                st.session_state.memoria.chat_memory.add_ai_message(resposta)
                
            except Exception as e:
                st.error(f"Erro na comunicação com o modelo: {e}")
                st.stop()

def main():
    with st.sidebar:
        sidebar()
    pagina_chat()

if __name__ == '__main__':
    main()