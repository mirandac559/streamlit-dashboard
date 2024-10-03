import pandas as pd
import streamlit as st
import plotly.express as px

# Carregar os dados
@st.cache
def load_data():
    data = pd.read_csv('houses_to_rent.csv')
    data['rent amount'] = data['rent amount'].replace({'R\$': '', ',': ''}, regex=True).astype(float)
    data['property tax'] = data['property tax'].replace({'R\$': '', ',': '', 'Incluso': '0', '-': '0'}, regex=True).astype(float)
    data['fire insurance'] = data['fire insurance'].replace({'R\$': '', ',': '', 'Incluso': '0', '-': '0'}, regex=True).astype(float)
    data['total'] = data['total'].replace({'R\$': '', ',': '', '-': '0'}, regex=True).astype(float)
    return data

data = load_data()

# Título do app
st.title("Dashboard Interativo de Imóveis para Aluguel")

# Filtro de cidade
city = st.selectbox("Selecione uma cidade:", data['city'].unique())

# Filtrar os dados pela cidade selecionada
filtered_data = data[data['city'] == city]

# Gráfico de Distribuição da Área
fig_area = px.histogram(filtered_data, x='area', nbins=30, title='Distribuição da Área dos Imóveis')
st.plotly_chart(fig_area)

# Gráfico de Correlação
fig_corr = px.scatter(filtered_data, x='rooms', y='rent amount', 
                       title='Correlação entre Quartos e Valor do Aluguel',
                       hover_data=['rent amount', 'area'])
st.plotly_chart(fig_corr)

# Gráfico de Total de Imóveis por Cidade
fig_total = px.bar(data, x='city', y='total', title='Total de Imóveis por Cidade')
st.plotly_chart(fig_total)

# Matriz de Correlação
corr_matrix = filtered_data.corr()
fig_matrix = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='Viridis', title='Matriz de Correlação')
st.plotly_chart(fig_matrix)
