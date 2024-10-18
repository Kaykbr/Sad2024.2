import streamlit as st
import pandas as pd
import plotly.express as px

# Título do aplicativo
st.title("Upload e Análise de Arquivo CSV de Candidatos")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Carregar o arquivo CSV
        df = pd.read_csv(uploaded_file, delimiter=';', encoding='ISO-8859-1')
    except pd.errors.ParserError:
        st.error("Erro ao ler o arquivo CSV.")
    else:
        st.success("Arquivo CSV carregado com sucesso!")

        # Sidebar para filtros dinâmicos
        st.sidebar.header("Filtros")

        # Filtro de Unidade Eleitoral
        unidade_eleitoral = st.sidebar.selectbox(
            "Escolha a Unidade Eleitoral",
            options=df['SG_UE'].unique(),
            help="Selecione a unidade eleitoral para filtrar os dados"
        )

        # Filtro de Cargo
        cargo = st.sidebar.selectbox(
            "Escolha o Cargo",
            options=df['DS_CARGO'].unique(),
            help="Selecione o cargo para filtrar os dados"
        )

        # Filtrar o dataframe com base nos filtros selecionados
        df_filtrado = df[(df['SG_UE'] == unidade_eleitoral) & (df['DS_CARGO'] == cargo)]
        
        # Mostrar uma prévia dos dados filtrados
        st.subheader(f"Prévia dos dados filtrados (Unidade Eleitoral: {unidade_eleitoral}, Cargo: {cargo})")
        st.write(df_filtrado.head(10))

        # Definir as colunas necessárias para os gráficos
        colunas_necessarias = ['DS_GRAU_INSTRUCAO', 'DS_GENERO', 'DS_COR_RACA', 'SG_PARTIDO']
        
        # Verificar se as colunas necessárias estão presentes no arquivo
        colunas_existentes = [col for col in colunas_necessarias if col in df_filtrado.columns]
        
        if len(colunas_existentes) < len(colunas_necessarias):
            st.error(f"As seguintes colunas estão faltando no arquivo CSV: {', '.join(colunas_necessarias)}")
        else:
            df = df[colunas_existentes].dropna()

            # Gráfico: Distribuição por Grau de Instrução (Sem Gradiente)
            st.subheader("Distribuição por Grau de Instrução")
            grau_instrucao_counts = df['DS_GRAU_INSTRUCAO'].value_counts().reset_index()
            grau_instrucao_counts.columns = ['Grau de Instrução', 'Contagem']
            fig_grau_instrucao = px.bar(
                grau_instrucao_counts, 
                x='Grau de Instrução', 
                y='Contagem', 
                title='Distribuição por Grau de Instrução', 
                labels={'Contagem':'Número de Candidatos', 'Grau de Instrução':'Grau de Instrução'}
            )
            st.plotly_chart(fig_grau_instrucao)

            # Gráfico: Relação entre Gênero e Grau de Instrução (Azul claro e escuro)
            st.subheader("Relação entre Gênero e Grau de Instrução")
            genero_instrucao = pd.crosstab(df['DS_GENERO'], df['DS_GRAU_INSTRUCAO']).reset_index()
            genero_instrucao_melted = genero_instrucao.melt(id_vars='DS_GENERO', var_name='Grau de Instrução', value_name='Contagem')
            fig_genero_instrucao = px.bar(
                genero_instrucao_melted, 
                x='Grau de Instrução', 
                y='Contagem', 
                color='DS_GENERO', 
                barmode='group', 
                title='Relação entre Gênero e Grau de Instrução',
                labels={'DS_GENERO':'Gênero', 'Contagem':'Número de Candidatos'},
                color_discrete_map={'FEMININO': '#aec7e8', 'MASCULINO': '#1f77b4'}  # Azul claro e escuro
            )
            st.plotly_chart(fig_genero_instrucao)

            # Gráfico: Distribuição de Cor/Raça (Cores Variadas)
            st.subheader("Distribuição de Cor/Raça")
            cor_raca_counts = df['DS_COR_RACA'].value_counts().reset_index()
            cor_raca_counts.columns = ['Cor/Raça', 'Contagem']
            fig_cor_raca = px.pie(
                cor_raca_counts, 
                names='Cor/Raça', 
                values='Contagem', 
                title='Distribuição de Cor/Raça', 
                hole=0.5,  # Gráfico de rosquinha
                color_discrete_map={
                    'PARDA': '#aec7e8', 'BRANCA': '#1f77b4', 'PRETA': '#Ff6f9c', 
                    'AMARELA': '#Ff4040', 'NÃO INFORMADO': '#90ee90', 'INDÍGENA': '#008080'
                }  # Cores variadas
            )
            st.plotly_chart(fig_cor_raca)

            # Gráfico: Distribuição por Gênero (Azul Claro e Escuro)
            st.subheader("Distribuição por Gênero")
            genero_counts = df['DS_GENERO'].value_counts().reset_index()
            genero_counts.columns = ['Gênero', 'Contagem']
            fig_genero = px.pie(
                genero_counts, 
                names='Gênero', 
                values='Contagem', 
                title='Distribuição por Gênero', 
                hole=0.5,  # Gráfico de rosquinha
                color_discrete_map={'FEMININO': '#aec7e8', 'MASCULINO': '#1f77b4'}  # Azul claro e escuro
            )
            st.plotly_chart(fig_genero)

            # Gráfico: Quantidade de Candidatas Mulheres por Partido (Cor Gradual Inversa)
            st.subheader("Quantidade de Candidatas Mulheres por Partido")
            mulheres_por_partido = df[df['DS_GENERO'] == 'FEMININO']['SG_PARTIDO'].value_counts().reset_index()
            mulheres_por_partido.columns = ['Partido', 'Contagem']
            fig_mulheres_partido = px.bar(
                mulheres_por_partido, 
                x='Partido', 
                y='Contagem',  # Barras verticais
                color='Contagem',  # Cor gradiente inversa
                title='Quantidade de Candidatas Mulheres por Partido',
                labels={'Contagem':'Número de Candidatas', 'Partido':'Sigla do Partido'},
                color_continuous_scale=px.colors.sequential.Blues_r  # Gradiente inverso (branco para mais, azul para menos)
            )
            st.plotly_chart(fig_mulheres_partido)

            # Gráfico: Quantidade de Candidatos Homens por Partido (Cor Gradual Inversa)
            st.subheader("Quantidade de Candidatos Homens por Partido")
            homens_por_partido = df[df['DS_GENERO'] == 'MASCULINO']['SG_PARTIDO'].value_counts().reset_index()
            homens_por_partido.columns = ['Partido', 'Contagem']
            fig_homens_partido = px.bar(
                homens_por_partido, 
                x='Partido', 
                y='Contagem',  # Barras verticais
                color='Contagem',  # Gradiente inverso de cor
                title='Quantidade de Candidatos Homens por Partido',
                labels={'Contagem':'Número de Candidatos', 'Partido':'Sigla do Partido'},
                color_continuous_scale=px.colors.sequential.Blues_r  # Gradiente inverso (branco para mais, azul para menos)
            )
            st.plotly_chart(fig_homens_partido)

            # Gráfico: Proporção de Candidatos Masculinos e Femininos por Partido (Empilhado)
            st.subheader("Proporção de Candidatos Masculinos e Femininos por Partido")
            proporcao_genero_partido = pd.crosstab(df['SG_PARTIDO'], df['DS_GENERO']).reset_index()
            proporcao_genero_partido['Total'] = proporcao_genero_partido['FEMININO'] + proporcao_genero_partido['MASCULINO']
            fig_proporcao_genero = px.bar(
                proporcao_genero_partido, 
                x='SG_PARTIDO', 
                y=['FEMININO', 'MASCULINO'],  # Barras empilhadas
                title='Proporção de Candidatos Masculinos e Femininos por Partido',
                labels={'value':'Quantidade de Candidatos', 'SG_PARTIDO':'Sigla do Partido'},
                color_discrete_map={'FEMININO': '#aec7e8', 'MASCULINO': '#1f77b4'},  # Cores azul claro e escuro
                hover_data=['Total'],  # Mostrar o total ao passar o mouse
                text_auto=True  # Exibir valores nas barras
            )
            fig_proporcao_genero.update_layout(barmode='stack', xaxis_tickangle=-45)  # Barras empilhadas e rotação dos rótulos
            st.plotly_chart(fig_proporcao_genero)

else:
    st.info("Por favor, faça o upload de um arquivo CSV.")
