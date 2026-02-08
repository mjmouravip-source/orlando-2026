import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mestre de Viagens", page_icon="✈️")

# Configuração Segura da API
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Erro: API Key não encontrada nos Secrets!")

# Mude de 'gemini-1.5-flash' para este formato completo:
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    system_instruction="""
    Você é o Analista de Logística e Guia de Viagens J&M Orlando.
    O Administrador Master é Joseana Tavares (CPF: 04492144609).
    Sua tarefa é extrair roteiros estruturados de PDFs/Excel e responder dúvidas de viagem.
    DIRETRIZES: 
    1. Foque em datas, horários e locais.
    2. Se houver vouchers, confirme códigos de reserva.
    3. Idioma: Português, mas mantenha nomes originais de parques e atrações.
    """
)

st.title("✈️ Mestre de Viagens")
cpf_input = st.text_input("Digite seu CPF para acessar:", type="password")

ADMIN_MASTER = "04492144609"

if cpf_input == ADMIN_MASTER:
    st.success("Acesso liberado, Administrador!")
    
    with st.sidebar:
        st.header("⚙️ Painel de Controle")
        arquivos_carregados = st.file_uploader("Subir roteiros (PDF/Excel)", accept_multiple_files=True)
        st.divider()
        st.info("Logado como: Yuri Mendonça")

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
            # O "Pulo do Gato": Criar a lista de partes corretamente
            conteudo_para_ia = []
            
            # 1. Adicionar os arquivos primeiro (se houver)
            if arquivos_carregados:
                for arq in arquivos_carregados:
                    bytes_data = arq.getvalue() # getvalue() é mais estável que read() no Streamlit
                    conteudo_para_ia.append({
                        "mime_type": arq.type,
                        "data": bytes_data
                    })
            
            # 2. Adicionar o texto por último
            conteudo_para_ia.append(prompt)
            
            try:
                # Gerar resposta
                response = model.generate_content(conteudo_para_ia)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Erro na IA: {e}")
                st.info("Dica: Verifique se os arquivos são PDF ou imagens suportadas.")

elif cpf_input != "":
    st.error("CPF não autorizado.")
