import streamlit as st
import google.generativeai as genai

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mestre de Viagens", page_icon="✈️", layout="centered")

# 1. CONFIGURAÇÃO DA API (Forçando estabilidade com transport='rest')
if "GEMINI_API_KEY" in st.secrets:
    # O uso do transport='rest' evita muitos erros 404/500 no Streamlit Cloud
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
else:
    st.error("Erro: API Key não encontrada nos Secrets do Streamlit!")
    st.stop()

# 2. DEFINIÇÃO DO MODELO (Usando nome estável)
# Usar 'gemini-1.5-flash' é o caminho mais seguro para evitar o erro NotFound
model = genai.GenerativeModel(
    model_name='gemini-1.5-pro',
    system_instruction="""
    Você é o Analista de Logística e Guia de Viagens J&M Orlando.
    O Administrador Master é Josi Tavares (CPF: 04492144609).
    Sua tarefa é extrair roteiros estruturados de PDFs/Excel e responder dúvidas de viagem.
    DIRETRIZES: 
    1. Foque em datas, horários e locais.
    2. Se houver vouchers, confirme códigos de reserva.
    3. Idioma: Português, mas mantenha nomes originais de parques e atrações.
    """
)

# INTERFACE
st.title("✈️ Mestre de Viagens - Orlando 2026")
cpf_input = st.text_input("Digite seu CPF para acessar:", type="password")

ADMIN_MASTER = "04492144609"

if cpf_input == ADMIN_MASTER:
    st.success("Bem-vindo, Administrador Josi!")
    
    with st.sidebar:
        st.header("⚙️ Painel de Controle")
        arquivos_carregados = st.file_uploader("Subir roteiros ou vouchers (PDF/Excel)", accept_multiple_files=True)
        st.divider()
        st.info("Status: Conectado ao Gemini 1.5 Flash")

    # Inicialização do Histórico
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibição do chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada de Usuário
    if prompt := st.chat_input("Pergunte sobre sua viagem..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            conteudo_para_ia = []
            
            # Processamento de Arquivos
            if arquivos_carregados:
                for arq in arquivos_carregados:
                    bytes_data = arq.getvalue()
                    conteudo_para_ia.append({
                        "mime_type": arq.type,
                        "data": bytes_data
                    })
            
            # Adiciona o texto por último
            conteudo_para_ia.append(prompt)
            
            try:
                # Gerar resposta da IA
                with st.spinner("Analisando roteiro..."):
                    response = model.generate_content(conteudo_para_ia)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                # Tratamento de erro detalhado
                if "404" in str(e):
                    st.error("Erro 404: Modelo não encontrado. Verifique se a API Key está ativa no Google Cloud Console.")
                else:
                    st.error(f"Erro na IA: {e}")

elif cpf_input != "":
    st.error("Acesso negado. CPF não autorizado.")
