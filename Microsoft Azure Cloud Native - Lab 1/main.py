import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()
BlobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
BlobContainerName = os.getenv("BLOB_CONTAINER_NAME")
blobacconuntName = os.getenv("BLOB_ACCOUNT_NAME")

SQL_Server = os.getenv("SQL_SERVER")
SQL_Database = os.getenv("SQL_DATABASE")
SQL_User = os.getenv("SQL_USER")
SQL_Password = os.getenv("SQL_PASSWORD")

st.title('Cadastro de Produtos')

#formularios de cadastro de produtos
product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do Produto")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

#salve o produto no banco de dados
def upload_blob(file):
    try:
        if file is None:
            st.error("Nenhum arquivo foi enviado.")
            return None

        blob_service_client = BlobServiceClient.from_connection_string(BlobConnectionString)
        container_client = blob_service_client.get_container_client(BlobContainerName)
        blob_name = str(uuid.uuid4()) + file.name  # Gera um nome único para o blob
        st.info(f"Nome do Blob: {blob_name}")  # Log do nome do Blob

        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.read(), overwrite=True)
        image_url = f"https://{blobacconuntName}.blob.core.windows.net/{BlobContainerName}/{blob_name}"
        st.info(f"URL gerada: {image_url}")  # Log do URL gerado
        return image_url
    except Exception as e:
        st.error(f"Erro ao fazer upload do arquivo: {type(e).__name__}: {e}")
        return None

def insert_product(product_name, product_price, product_description, product_image):
    try:
        imagem_url = upload_blob(product_image)
        conn = pymssql.connect(server=SQL_Server, user=SQL_User, password=SQL_Password, database=SQL_Database)
        cursor = conn.cursor()
        cursor.execute(f"insert into produtos (nome, preco, descricao, imagem_url) values ('{product_name}', {product_price}, '{product_description}', '{imagem_url}')")
        conn.commit()
        conn.close()
        st.success("Produto cadastrado com sucesso!")
        return True
    except Exception as e:
        st.error(f"Erro ao cadastrar produto: {type(e).__name__} - {e}")
        return False
    
def list_products():
    try:
        conn = pymssql.connect(server=SQL_Server, user=SQL_User, password=SQL_Password, database=SQL_Database)
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, descricao, preco, imagem_url FROM Produtos")
        
        columns = [col[0] for col in cursor.description]  # Pega os nomes das colunas
        rows = cursor.fetchall()
        conn.close()

        # Transforma cada linha em um dicionário {coluna: valor}
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        st.error(f'Erro ao listar produtos: {e}')
        return []


def list_produtos_screen():
    products = list_products()
    if products:
        # Define o número de cards por linha
        cards_por_linha = 3
        # Cria as colunas iniciais
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product['nome']}")
                st.write(f"**Descrição:** {product['descricao']}")
                st.write(f"**Preço:** R$ {product['preco']:.2f}")
                if product["imagem_url"]:
                    html_img = f'<img src="{product["imagem_url"]}" width="200" height="200" alt="Imagem do produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("---")
            # A cada 'cards_por_linha' produtos, se ainda houver produtos, cria novas colunas
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto encontrado.")

if st.button("Cadastrar Produto"):
    insert_product(product_name, product_price, product_description, product_image)
    retur_message = "Produto cadastrado com sucesso!"

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
    list_produtos_screen()
    #list_produtos_screen() 
    retur_message = "Produto listados com sucesso!"

