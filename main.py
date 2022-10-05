import streamlit as st
import pandas as pd

st.markdown("<center><h1>Fakenews - Análise de Imagens</h1><center>", unsafe_allow_html=True)
st.markdown('<center><h4>DashBoard</h4><center>', unsafe_allow_html=True)

df_wpp = pd.read_csv('./wpp.csv', sep=';')
df_wpp['date_message'] = pd.to_datetime(df_wpp['date_message'], format = "%Y-%m-%d %H:%M:%S")

min_date = df_wpp['date_message'].min()
max_date = df_wpp['date_message'].max()

with st.sidebar:
    st.sidebar.title("Filtros")
    st.sidebar.header("Top: ")
    top = st.slider('TOP: ', 5, 100, 10)
    st.markdown('---')
    st.sidebar.header("Filtros de datas: ")
    st.markdown(f"<h5>Data Mínima: {min_date.strftime('%d/%m/%Y')}</h5>", unsafe_allow_html=True)
    start_date = st.date_input(
        "Data Inicial (Formato: Y/m/d)",
        value = pd.to_datetime(min_date, format="%d/%m/%Y"),
        min_value=pd.to_datetime(min_date, format="%d/%m/%Y"),
        max_value = pd.to_datetime(max_date, format="%d/%m/%Y")
    )
    st.markdown(f"<h5>Data Máxima: {max_date.strftime('%d/%m/%Y')}</h5>", unsafe_allow_html=True)
    end_date = st.date_input(
        "Data Final (Formato: Y/m/d)",
        value = pd.to_datetime(max_date, format="%Y-%m-%d"),
        min_value=pd.to_datetime(start_date, format="%Y-%m-%d"),
        max_value = pd.to_datetime(max_date, format="%Y-%m-%d")
    )

start_date = str(start_date)
end_date = str(end_date)


print("Data inicial: ", start_date)
print("Data Final: ", end_date)


df_wpp = df_wpp.loc[(df_wpp['date_message'] >= start_date) & (df_wpp['date_message'] <= end_date)]
df_group = df_wpp.groupby(by=['media']).agg('count').sort_values(by='id', ascending=False)
df_group.reset_index(inplace=True)
df_group = df_group[['media', 'id']]
df_group.rename(columns={'id': 'count', 'media': 'imagem'}, inplace=True)

st.markdown(f"<center><h3>TOP {top} de imagens mais compartilhadas</h3></center>", unsafe_allow_html=True)
st.markdown('---')

for i in range(top):
    #print(i)
    print(df_group.iloc[i])
    midia = df_group.iloc[i]['imagem']
    qntd  = df_group.iloc[i]['count']
    print(midia, qntd)
    st.markdown(f"<center><h3>Imagem: {midia}</h3></center>", unsafe_allow_html=True)
    st.markdown(f"<center><h3>Quantidade de compartilhamento: {qntd}</h3></center>", unsafe_allow_html=True)
    st.markdown(f'<center><img src="https://api.faroldigital.info/file?name={midia}" width="500" height="300"></center>', unsafe_allow_html=True)
    st.markdown('---')