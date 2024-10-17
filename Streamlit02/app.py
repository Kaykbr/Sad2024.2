import streamlit as st
import pandas as pd

st.title("Upload e Prévia de Arquivo CSV")

uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except pd.errors.ParserError:
        try:
            df = pd.read_csv(uploaded_file, delimiter=';')
        except pd.errors.ParserError:
            df = pd.read_csv(uploaded_file, error_bad_lines=False)
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
        except pd.errors.ParserError:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', delimiter=';')

    st.success("Arquivo CSV carregado com sucesso!")
    
    st.subheader("Prévia dos dados (primeiras 10 linhas):")
    st.write(df.head(10)) 
else:
    st.info("Por favor, faça o upload de um arquivo CSV.")
