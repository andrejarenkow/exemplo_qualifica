import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

st.title("Upload de Arquivo para Google Drive")

# ====== CONFIGURAÇÕES ======
# Caminho do arquivo JSON da service account
SERVICE_ACCOUNT_FILE = "service_account.json"

# ID da pasta no Google Drive onde os arquivos serão salvos
FOLDER_ID = "COLOQUE_AQUI_O_ID_DA_PASTA"

# Autenticando no Google Drive
@st.cache_resource
def conectar_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=creds)

drive_service = conectar_drive()

uploaded_file = st.file_uploader("Selecione um arquivo", type=None)

if uploaded_file:
    st.write("Arquivo carregado:", uploaded_file.name)

    if st.button("Enviar para o Google Drive"):
        try:
            file_metadata = {
                "name": uploaded_file.name,
                "parents": [FOLDER_ID]
            }

            media = MediaIoBaseUpload(
                io.BytesIO(uploaded_file.read()),
                mimetype=uploaded_file.type,
                resumable=True
            )

            arquivo = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()

            st.success(f"Arquivo enviado com sucesso! ID: {arquivo['id']}")
        
        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
