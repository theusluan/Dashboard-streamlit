import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Supermarket Sales")
st.set_page_config(layout="wide")

try:
    df = pd.read_csv(r"C:\Users\MTX\Desktop\supermarket_sales.csv", sep=";", decimal=",")

    # Converter coluna de data
    df["Date"] = pd.to_datetime(df["Date"])
    # Ordernar pela data antiga -> recente.
    df=df.sort_values("Date")

    st.success("Arquivo carregado com sucesso!")
   
except Exception as e:
    st.error("Erro ao carregar o arquivo:")
    st.write(e)

# Criando uma sidebar com meses unicos de maneira vetorizada
df["Month"] = df["Date"].dt.to_period("M").astype(str)
month = st.sidebar.selectbox("Mês", df["Month"].unique())
df_filtered = df[df["Month"] == month]

# st.dataframe(df_filtered, use_container_width=True) Caso queira que apareça a tabela completa.


col1, col2 =  st.columns(2)
col3, col4, col5 = st.columns(3)

# Qual o faturamento por dia.
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Qual o faturamento por produto.
fig_prod = px.bar(df_filtered, x="Date", y="Product line", 
                  color="City", title="Faturamento por produto",
                  orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

# Qual o faturamento feito por filial.
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total",
                   title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Faturamento por tipo de pagamento.
fig_pay = px.pie(
    df_filtered.groupby("Payment")["Total"].sum().reset_index(),
    names="Payment",
    values="Total",
    hole=0.1,
    title="Faturamento por tipo de pagamento"
    
)
col4.plotly_chart(fig_pay, use_container_width=True)

# Avaliações das filiais.
city_total = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(city_total, x="City", y="Rating",
             title="Avaliações das filiais")
col5.plotly_chart(fig_rating, use_container_width=True)