import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Upload e Análise de Arquivo CSV de Candidatos")

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
    
    # Exibir a prévia dos dados
    st.subheader("Prévia dos dados (primeiras 10 linhas):")
    st.write(df.head(10))
    
    # Filtrando as colunas que vamos utilizar
    colunas_necessarias = [
        'DS_GRAU_INSTRUCAO', 'DS_GENERO', 'DS_COR_RACA', 
        'SG_PARTIDO', 'DS_GENERO'
    ]
    
    # Verificando se as colunas necessárias estão presentes
    df = df[colunas_necessarias].dropna()

    st.subheader("Distribuição por Grau de Instrução")
    grau_instrucao_counts = df['DS_GRAU_INSTRUCAO'].value_counts()
    st.bar_chart(grau_instrucao_counts)

    st.subheader("Relação entre Gênero e Grau de Instrução")
    genero_instrucao = pd.crosstab(df['DS_GENERO'], df['DS_GRAU_INSTRUCAO'])
    st.write(genero_instrucao)
    st.bar_chart(genero_instrucao)

    st.subheader("Distribuição de Cor/Raça")
    cor_raca_counts = df['DS_COR_RACA'].value_counts()
    st.bar_chart(cor_raca_counts)

    st.subheader("Distribuição por Gênero")
    genero_counts = df['DS_GENERO'].value_counts()
    st.bar_chart(genero_counts)

    st.subheader("Quantidade de Candidatas Mulheres por Partido")
    mulheres_por_partido = df[df['DS_GENERO'] == 'FEMININO']['SG_PARTIDO'].value_counts()
    st.bar_chart(mulheres_por_partido)

    st.subheader("Quantidade de Candidatos Homens por Partido")
    homens_por_partido = df[df['DS_GENERO'] == 'MASCULINO']['SG_PARTIDO'].value_counts()
    st.bar_chart(homens_por_partido)

    st.subheader("Proporção de Candidatos Masculinos e Femininos por Partido")
    proporcao_genero_partido = pd.crosstab(df['SG_PARTIDO'], df['DS_GENERO'], normalize='index') * 100
    st.write(proporcao_genero_partido)
    st.bar_chart(proporcao_genero_partido)
    
else:
    st.info("Por favor, faça o upload de um arquivo CSV.")
