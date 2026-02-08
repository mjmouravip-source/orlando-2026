import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mestre de Viagens", page_icon="✈️")

# Configuração Segura da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Erro: API Key não encontrada nos Secrets!")

model = genai.GenerativeModel('gemini-1.5-flash')

st.title("✈️ Mestre de Viagens")
cpf_input = st.text_input("Digite seu CPF para acessar:", type="password")

ADMIN_MASTER = "04492144609"

if cpf_input == ADMIN_MASTER:
    st.success("Acesso liberado, Administrador!")
    
    with st.sidebar:
        st.header("⚙️ Painel de Controle")
        # Upload de arquivos
        arquivos_carregados = st.file_uploader("Subir roteiros (PDF/Excel)", accept_multiple_files=True)
        
        st.divider()
        st.info("Funcionalidades: \n1. Roteiro Dia a Dia\n2. Câmbio e Cultura\n3. Relatório de Memórias")

    # Inicia histórico de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostra mensagens anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Entrada do usuário
    if prompt := st.chat_input("Como posso ajudar na sua viagem?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Lógica para incluir os arquivos no processamento
            conteudo_para_ia = [prompt]
            
            if arquivos_carregados:
                for arq in arquivos_carregados:
                    # Lê o arquivo e adiciona à lista para o Gemini
                    bytes_data = arq.read()
                    conteudo_para_ia.append({"mime_type": arq.type, "data": bytes_data})
            
            # Resposta da IA considerando os arquivos
            response = model.generate_content(conteudo_para_ia)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

elif cpf_input != "":
    st.error("CPF não autorizado.")
