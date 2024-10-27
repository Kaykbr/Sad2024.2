import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

st.set_page_config(page_title='Análise Climática Global', page_icon='🌍', layout='wide')

st.title('Dashboard de Análise Climática Global')

st.sidebar.title('Carregamento de Dados')

uploaded_temp = st.sidebar.file_uploader("Carregue o arquivo de Temperaturas (GlobalLandTemperaturesByCountry.csv)", type=["csv"])
uploaded_co2 = st.sidebar.file_uploader("Carregue o arquivo de Emissões de CO₂ (GCB2022v27_MtCO2_flat.csv)", type=["csv"])

if uploaded_temp is not None and uploaded_co2 is not None:
    temp_data = pd.read_csv(uploaded_temp)
    co2_data = pd.read_csv(uploaded_co2)

    temp_data = temp_data[['dt', 'AverageTemperature', 'Country']]
    temp_data = temp_data.dropna(subset=['AverageTemperature'])
    temp_data['Year'] = pd.to_datetime(temp_data['dt']).dt.year
    temp_data = temp_data[temp_data['Year'] >= 1960]

    def standardize_country_name(name):
        try:
            return pycountry.countries.lookup(name).name
        except LookupError:
            return name  
    temp_data['Country'] = temp_data['Country'].apply(standardize_country_name)

    co2_data = co2_data[['Country', 'Year', 'Total']]
    co2_data = co2_data.rename(columns={'Total': 'CO2Emissions'})
    co2_data = co2_data.dropna(subset=['CO2Emissions'])

    co2_data['Country'] = co2_data['Country'].apply(standardize_country_name)

    temp_data['Year'] = temp_data['Year'].astype(int)
    co2_data['Year'] = co2_data['Year'].astype(int)

    merged_data = pd.merge(temp_data, co2_data, on=['Country', 'Year'], how='inner')

    if merged_data.empty:
        st.error("Nenhum dado disponível após a mesclagem dos datasets. Verifique se os nomes dos países correspondem e se há anos em comum.")
    else:
        st.sidebar.title('Filtros')

        countries = merged_data['Country'].unique()
        selected_countries = st.sidebar.multiselect('Selecione os países:', sorted(countries), default=['Brazil', 'United States', 'China', 'India'])

        years = merged_data['Year'].unique()
        selected_years = st.sidebar.slider('Selecione o intervalo de anos:', int(years.min()), int(years.max()), (1990, 2020))

        filtered_data = merged_data[
            (merged_data['Country'].isin(selected_countries)) &
            (merged_data['Year'] >= selected_years[0]) &
            (merged_data['Year'] <= selected_years[1])
        ]

        if filtered_data.empty:
            st.warning("Nenhum dado disponível para os filtros selecionados.")
        else:
            menu = ['Visão Geral', 'Análise Detalhada']
            choice = st.sidebar.selectbox('Selecione a página:', menu)

            if choice == 'Visão Geral':
                st.header('Visão Geral')

                # Gráfico 1: Mapa Coroplético de Temperatura Média por País
                st.subheader('Temperatura Média Global')
                avg_temp_country = filtered_data.groupby('Country')['AverageTemperature'].mean().reset_index()
                fig_map = px.choropleth(avg_temp_country, locations='Country', locationmode='country names',
                                        color='AverageTemperature', color_continuous_scale='RdYlBu_r',
                                        title='Temperatura Média por País',
                                        labels={'AverageTemperature': 'Temperatura Média (°C)'})
                st.plotly_chart(fig_map, use_container_width=True)

                # Gráfico 2: Emissões Totais de CO₂ por País (Gráfico de Pizza)
                st.subheader('Emissões Totais de CO₂ por País')
                total_co2_country = filtered_data.groupby('Country')['CO2Emissions'].sum().reset_index()
                fig_pie = px.pie(total_co2_country, names='Country', values='CO2Emissions',
                                 title='Participação nas Emissões Totais de CO₂')
                st.plotly_chart(fig_pie, use_container_width=True)

                # Valor Total: Emissões Globais no Período Selecionado
                total_co2_global = total_co2_country['CO2Emissions'].sum()
                st.metric('Emissões Totais de CO₂ no Período Selecionado (MtCO₂)', f"{total_co2_global:.2f}")

            elif choice == 'Análise Detalhada':
                st.header('Análise Detalhada')

                # Gráfico 3: Temperatura Média ao Longo do Tempo
                st.subheader('Temperatura Média ao Longo do Tempo')
                fig_line_temp = px.line(filtered_data, x='Year', y='AverageTemperature', color='Country',
                                        title='Evolução da Temperatura Média')
                st.plotly_chart(fig_line_temp, use_container_width=True)

                # Gráfico 4: Emissões de CO₂ ao Longo do Tempo
                st.subheader('Emissões de CO₂ ao Longo do Tempo')
                fig_line_co2 = px.line(filtered_data, x='Year', y='CO2Emissions', color='Country',
                                       title='Evolução das Emissões de CO₂')
                st.plotly_chart(fig_line_co2, use_container_width=True)

                # Gráfico 5: Relação entre Temperatura Média e Emissões de CO₂
                st.subheader('Relação entre Temperatura Média e Emissões de CO₂')
                fig_scatter = px.scatter(filtered_data, x='CO2Emissions', y='AverageTemperature', color='Country',
                                         trendline='ols', title='Temperatura Média vs Emissões de CO₂')
                st.plotly_chart(fig_scatter, use_container_width=True)

                # Tabela de Dados Filtrados
                st.subheader('Dados Filtrados')
                st.dataframe(filtered_data)

                # Valor Total: Temperatura Média no Período Selecionado
                avg_temp_global = filtered_data['AverageTemperature'].mean()
                st.metric('Temperatura Média no Período Selecionado (°C)', f"{avg_temp_global:.2f}")

else:
    st.info('Por favor, carregue os dois arquivos CSV para iniciar a análise.')
