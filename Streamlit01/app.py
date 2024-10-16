import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('vendas.csv', sep=';', decimal=',')

def filtrar_por_mes(df, mes_selecionado):
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    ano, mes = map(int, mes_selecionado.split('-'))

    df_filtrado = df[(df['Date'].dt.year == ano) & (df['Date'].dt.month == mes)]
    return df_filtrado

def vendas_page(df, mes_selecionado):
    st.title('Página de Vendas')

    df_filtrado = filtrar_por_mes(df, mes_selecionado)

    col1, col2 = st.columns([1, 1])  

    # Gráfico 1: Faturamento por dia, empilhado por cidade
    with col1:
        faturamento_dia_cidade = df_filtrado.groupby(['Date', 'City'])['Total'].sum().reset_index()
        fig1 = px.bar(faturamento_dia_cidade, x='Date', y='Total', color='City', title='Faturamento Diário por Cidade',
                      labels={'Total': 'Faturamento', 'Date': 'Data'}, barmode='stack', width=2000, height=400)  
        st.plotly_chart(fig1) 

    # Gráfico 2: Faturamento por linha de produto, empilhado por cidade
    with col2:
        faturamento_produto_cidade = df_filtrado.groupby(['Product line', 'City'])['Total'].sum().reset_index()
        fig2 = px.bar(faturamento_produto_cidade, x='Total', y='Product line', color='City', title='Faturamento por Linha de Produto e Cidade',
                      labels={'Total': 'Faturamento', 'Product line': 'Linha de Produto'}, orientation='h', barmode='stack', width=2000, height=400)  
        st.plotly_chart(fig2)
    st.markdown("---")

    col3, col4, col5 = st.columns([1, 1, 1])  

    # Gráfico 3: Faturamento por cidade
    with col3:
        faturamento_cidade = df_filtrado.groupby('City')['Total'].sum().reset_index()
        fig3 = px.bar(faturamento_cidade, x='City', y='Total', title='Faturamento por Cidade', height=400) 
        st.plotly_chart(fig3, use_container_width=True)
 

    # Gráfico 4: Faturamento por tipo de pagamento (gráfico de pizza)
    with col4:
        faturamento_pagamento = df_filtrado.groupby('Payment')['Total'].sum().reset_index()
        fig4 = px.pie(faturamento_pagamento, values='Total', names='Payment', title='Faturamento por Tipo de Pagamento', height=400) 
        st.plotly_chart(fig4, use_container_width=True)

    # Gráfico 5: Avaliação média por cidade
    with col5:
        avaliacao_cidade = df_filtrado.groupby('City')['Rating'].mean().reset_index()
        fig5 = px.bar(avaliacao_cidade, x='City', y='Rating', title='Avaliação Média por Cidade', height=400)  
        st.plotly_chart(fig5, use_container_width=True)

def pagina_exemplo_1():
    st.title('Página Exemplo 1')
    st.write("Conteúdo da Página Exemplo 1")

def pagina_exemplo_2():
    st.title('Página Exemplo 2')
    st.write("Conteúdo da Página Exemplo 2")

df = load_data()

st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Selecione a página", ["Vendas", "Página Exemplo 1", "Página Exemplo 2"])

mes_selecionado = st.sidebar.selectbox(
    'Selecione o Mês (Formato: Ano-Mês)',
    [f'{ano}-{mes}' for ano in range(2019, 2023) for mes in range(1, 13)]
)

# Exibir a página selecionada
if pagina == 'Vendas':
    vendas_page(df, mes_selecionado)
elif pagina == 'Página Exemplo 1':
    pagina_exemplo_1()
elif pagina == 'Página Exemplo 2':
    pagina_exemplo_2()
