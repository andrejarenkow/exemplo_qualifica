import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

st.title("Upload de Arquivo para Google Drive")

# ========== CONECTAR AO GOOGLE DRIVE VIA SECRETS ==========
@st.cache_resource
def conectar_drive():
    # pega o bloco [google_service_account] do secrets.toml
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["google_service_account"]
    )

    service = build("drive", "v3", credentials=creds)
    return service

drive_service = conectar_drive()

# ID da pasta no Google Drive (pode colocar no secrets também)
FOLDER_ID = st.secrets["folder_id"]

# ========== UPLOAD ==========
uploaded_file = st.file_uploader("Selecione um arquivo para enviar:")

if uploaded_file:
    st.write(f"Arquivo carregado: **{uploaded_file.name}**")

    if st.button("Enviar para o Google Drive"):
        try:
            # Metadados do arquivo
            file_metadata = {
                "name": uploaded_file.name,
                "parents": [FOLDER_ID]
            }

            # Conteúdo do arquivo
            media = MediaIoBaseUpload(
                io.BytesIO(uploaded_file.read()),
                mimetype=uploaded_file.type,
                resumable=True
            )

            # Enviar para o Drive
            arquivo = drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id, name"
            ).execute()

            st.success(f"Arquivo enviado com sucesso! ID: {arquivo['id']}")

        except Exception as e:
            st.error(f"Erro ao enviar: {e}")
