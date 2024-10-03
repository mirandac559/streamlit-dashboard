import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados
@st.cache
def load_data():
    data = pd.read_csv('houses_to_rent_v2.csv')
    return data

data = load_data()

# Função para limpar e converter colunas numéricas
def clean_numeric_column(column):
    column = column.replace({'R\$': '', ',': '', 'Incluso': '0', '-': '0'}, regex=True)
    return pd.to_numeric(column, errors='coerce')

# Remover prefixos 'R$' e tratar valores não numéricos
data['property tax'] = clean_numeric_column(data['property tax'])
data['fire insurance'] = clean_numeric_column(data['fire insurance'])
data['rent amount'] = clean_numeric_column(data['rent amount'])
data['total'] = clean_numeric_column(data['total'])

# Título do app
st.title("Dashboard Interativo de Imóveis para Aluguel")

# Filtro de cidade
city = st.selectbox("Selecione uma cidade:", data['city'].unique())

# Filtrar os dados pela cidade selecionada
filtered_data = data[data['city'] == city]

# Exibir os tipos de dados e as primeiras linhas dos dados filtrados
st.write(filtered_data.dtypes)  # Verifique os tipos de dados das colunas
st.write(filtered_data.head())    # Veja as primeiras linhas dos dados filtrados

# Verifique se há colunas numéricas antes de calcular a correlação
numeric_columns = filtered_data.select_dtypes(include=['float64', 'int64']).columns

if len(numeric_columns) > 0:
    # Gráfico de Distribuição da Área
    fig_area = px.histogram(filtered_data, x='area', nbins=30, title='Distribuição da Área dos Imóveis')
    st.plotly_chart(fig_area)

    # Gráfico de Correlação
    if 'rooms' in numeric_columns and 'rent amount' in numeric_columns:
        fig_corr = px.scatter(filtered_data, x='rooms', y='rent amount', 
                               title='Correlação entre Quartos e Valor do Aluguel',
                               hover_data=['rent amount', 'area'])
        st.plotly_chart(fig_corr)

    # Matriz de Correlação
    corr_matrix = filtered_data[numeric_columns].corr()
    fig_matrix = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='Viridis', title='Matriz de Correlação')
    st.plotly_chart(fig_matrix)
else:
    st.warning("Não há colunas numéricas suficientes para calcular a correlação.")
