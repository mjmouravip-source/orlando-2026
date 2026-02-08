import streamlit as st
import google.generativeai as genai

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Mestre de Viagens", page_icon="✈️")

# CONFIGURAÇÃO DA IA (A chave será configurada no painel do Streamlit depois)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Configure a API Key nas Secrets!")

model = genai.GenerativeModel('gemini-1.5-pro')

# INTERFACE DE LOGIN
st.title("✈️ Mestre de Viagens")
cpf_input = st.text_input("Digite seu CPF para acessar:", type="password")

# BANCO DE DADOS SIMPLIFICADO (CPFs Autorizados)
ADMIN_MASTER = "04492144609"
AUTORIZADOS = [ADMIN_MASTER, "12345678900"] # Adicione outros aqui

if cpf_input in AUTORIZADOS:
    st.success(f"Acesso liberado!")
    
    # MENU LATERAL
    with st.sidebar:
        st.header("⚙️ Painel de Controle")
        if cpf_input == ADMIN_MASTER:
            st.subheader("Modo Administrador")
            arquivos = st.file_uploader("Subir roteiros (PDF/Excel)", accept_multiple_files=True)
        
        st.divider()
        st.info("Funcionalidades: \n1. Roteiro Dia a Dia\n2. Câmbio e Cultura\n3. Relatório de Memórias")

    # CHAT/INTERAÇÃO
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Como posso ajudar na sua viagem?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Aqui enviamos o prompt para o Gemini com as suas instruções
            full_prompt = f"Instrução: Você é um guia de viagem. O usuário é {cpf_input}. Responda de forma curta e use voz se necessário. \nPergunta: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

elif cpf_input != "":
    st.error("CPF não autorizado. Fale com o administrador master.")
