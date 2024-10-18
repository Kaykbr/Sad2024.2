import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Upload e Análise de Arquivo CSV de Candidatos")

uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, delimiter=';', encoding='ISO-8859-1')
    except pd.errors.ParserError:
        st.error("Erro ao ler o arquivo CSV.")
    else:
        st.success("Arquivo CSV carregado com sucesso!")
        
        # Exibir a prévia dos dados
        st.subheader("Prévia dos dados (primeiras 10 linhas):")
        st.write(df.head(10))

        # Colunas que vamos utilizar
        colunas_necessarias = [
            'DS_GRAU_INSTRUCAO', 'DS_GENERO', 'DS_COR_RACA', 'SG_PARTIDO'
        ]
        
        # Verificando se as colunas necessárias estão presentes
        colunas_existentes = [col for col in colunas_necessarias if col in df.columns]
        
        if len(colunas_existentes) < len(colunas_necessarias):
            st.error(f"As seguintes colunas estão faltando no arquivo CSV: {', '.join(colunas_necessarias)}")
        else:
            df = df[colunas_existentes].dropna()

            # Gráfico de Distribuição por Grau de Instrução
            st.subheader("Distribuição por Grau de Instrução")
            grau_instrucao_counts = df['DS_GRAU_INSTRUCAO'].value_counts().reset_index()
            grau_instrucao_counts.columns = ['Grau de Instrução', 'Contagem']
            fig_grau_instrucao = px.bar(grau_instrucao_counts, 
                                        x='Grau de Instrução', 
                                        y='Contagem', 
                                        title='Distribuição por Grau de Instrução', 
                                        labels={'Contagem':'Número de Candidatos', 'Grau de Instrução':'Grau de Instrução'})
            st.plotly_chart(fig_grau_instrucao)

            # Gráfico da Relação entre Gênero e Grau de Instrução
            st.subheader("Relação entre Gênero e Grau de Instrução")
            genero_instrucao = pd.crosstab(df['DS_GENERO'], df['DS_GRAU_INSTRUCAO']).reset_index()
            genero_instrucao_melted = genero_instrucao.melt(id_vars='DS_GENERO', var_name='Grau de Instrução', value_name='Contagem')
            fig_genero_instrucao = px.bar(genero_instrucao_melted, 
                                          x='Grau de Instrução', 
                                          y='Contagem', 
                                          color='DS_GENERO', 
                                          barmode='group', 
                                          title='Relação entre Gênero e Grau de Instrução',
                                          labels={'DS_GENERO':'Gênero', 'Contagem':'Número de Candidatos'})
            st.plotly_chart(fig_genero_instrucao)

            # Gráfico de Distribuição de Cor/Raça
            st.subheader("Distribuição de Cor/Raça")
            cor_raca_counts = df['DS_COR_RACA'].value_counts().reset_index()
            cor_raca_counts.columns = ['Cor/Raça', 'Contagem']
            fig_cor_raca = px.bar(cor_raca_counts, 
                                  x='Cor/Raça', 
                                  y='Contagem', 
                                  title='Distribuição de Cor/Raça', 
                                  labels={'Contagem':'Número de Candidatos', 'Cor/Raça':'Cor/Raça'})
            st.plotly_chart(fig_cor_raca)

            # Gráfico de Distribuição por Gênero
            st.subheader("Distribuição por Gênero")
            genero_counts = df['DS_GENERO'].value_counts().reset_index()
            genero_counts.columns = ['Gênero', 'Contagem']
            fig_genero = px.bar(genero_counts, 
                                x='Gênero', 
                                y='Contagem', 
                                title='Distribuição por Gênero', 
                                labels={'Contagem':'Número de Candidatos', 'Gênero':'Gênero'})
            st.plotly_chart(fig_genero)

            # Gráfico da Quantidade de Candidatas Mulheres por Partido
            st.subheader("Quantidade de Candidatas Mulheres por Partido")
            mulheres_por_partido = df[df['DS_GENERO'] == 'FEMININO']['SG_PARTIDO'].value_counts().reset_index()
            mulheres_por_partido.columns = ['Partido', 'Contagem']
            fig_mulheres_partido = px.bar(mulheres_por_partido, 
                                          x='Partido', 
                                          y='Contagem', 
                                          title='Quantidade de Candidatas Mulheres por Partido',
                                          labels={'Contagem':'Número de Candidatas', 'Partido':'Partido'})
            st.plotly_chart(fig_mulheres_partido)

            # Gráfico da Quantidade de Candidatos Homens por Partido
            st.subheader("Quantidade de Candidatos Homens por Partido")
            homens_por_partido = df[df['DS_GENERO'] == 'MASCULINO']['SG_PARTIDO'].value_counts().reset_index()
            homens_por_partido.columns = ['Partido', 'Contagem']
            fig_homens_partido = px.bar(homens_por_partido, 
                                        x='Partido', 
                                        y='Contagem', 
                                        title='Quantidade de Candidatos Homens por Partido',
                                        labels={'Contagem':'Número de Candidatos', 'Partido':'Partido'})
            st.plotly_chart(fig_homens_partido)

            # Gráfico da Proporção de Candidatos Masculinos e Femininos por Partido
            st.subheader("Proporção de Candidatos Masculinos e Femininos por Partido")
            proporcao_genero_partido = pd.crosstab(df['SG_PARTIDO'], df['DS_GENERO'], normalize='index').reset_index()
            proporcao_genero_partido_melted = proporcao_genero_partido.melt(id_vars='SG_PARTIDO', var_name='Gênero', value_name='Proporção')
            fig_proporcao_genero = px.bar(proporcao_genero_partido_melted, 
                                          x='SG_PARTIDO', 
                                          y='Proporção', 
                                          color='Gênero', 
                                          barmode='group', 
                                          title='Proporção de Candidatos Masculinos e Femininos por Partido',
                                          labels={'SG_PARTIDO':'Partido', 'Proporção':'Proporção (%)'})
            st.plotly_chart(fig_proporcao_genero)
else:
    st.info("Por favor, faça o upload de um arquivo CSV.")
