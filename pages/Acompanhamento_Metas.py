import pandas as pd
import streamlit as st
from login import check_password
from datetime import datetime, date
import altair as alt

st.set_page_config(page_title="Resultados Warren Rena", page_icon="assets/LogoW.png", layout="wide", initial_sidebar_state="expanded")
st.logo("assets/LogoWarrenRena.png", icon_image="assets/LogoWRena.png")

if not check_password():
    st.stop()

df = st.session_state['df']

st.title(':material/target: Acompanhamento Metas')
st.subheader("Em desenvolvimento :material/engineering:")

with st.sidebar:
    st.subheader("Filtro :material/filter_list:")
    with st.expander("Selecione a mesa:"):
        st.write("OI")
        
    st.write("---")
    if st.button("Logout"):
        st.session_state['password_correct'] = False
        st.rerun()

df_feriados = pd.read_excel("data/MetasEFeriados.xlsx", sheet_name="Feriados")
df_feriados['Data'] = pd.to_datetime(df_feriados['Data']).dt.date
df_metas = pd.read_excel("data/MetasEFeriados.xlsx", sheet_name="Metas")

ano_atual = datetime.today().year
ano_anterior = datetime.today().year -1

df_ano_atual = df[(df['reference_day'] >= date(ano_atual, 1, 1)) & (df['reference_day'] <= date(ano_atual, 12, 31))]
df_ano_anterior = df[(df['reference_day'] >= date(ano_anterior, 1, 1)) & (df['reference_day'] <= date(ano_anterior, 12, 31))]
df_ano_anterior_data_atual = df_ano_anterior[df_ano_anterior["month_day"] >= df_ano_atual["month_day"].max()]
receita_ano_atual = df_ano_atual["revenue"].sum()
receita_ano_anterior = df_ano_anterior_data_atual['revenue'].sum()
st.metric(
    "Receita anual até o momento", 
    value=f"{receita_ano_atual:,.2f}",  # Formata com separador de milhar e 2 casas decimais
    delta=f"{(receita_ano_atual - receita_ano_anterior):,.2f}"  # Mesmo formato para a diferença
)

gran4 = "month"
granularidade4 = st.pills(f"Comparação de Receita {ano_atual} x {ano_anterior}", ["Mês","Semana"], selection_mode="single", default="Mês",key="receita_YOY")
if granularidade4 == "Semana":
    gran4 = "week"
elif granularidade4 == "Mês":
    gran4 = "month"

# df4 = df.groupby([gran4, "month"])["revenue"].sum().reset_index()

# # Converter mês para string para que o eixo X o trate corretamente
# df4[gran4] = df4[gran4].astype(str)

# chart = alt.Chart(df4).mark_line(strokeWidth=3).encode(
#     x=alt.X(f"{gran4}:N", title=f"{granularidade4}", sort=list(map(str, range(1, 13)))),
#     y=alt.Y('revenue:Q', title="Receita"),
#     color=alt.Color(f"{gran4}:N", title="Ano", legend=alt.Legend(orient="bottom")),
#     tooltip=[
#         alt.Tooltip(f"{gran4}:N", title="Mês"),
#         alt.Tooltip('year:N', title="Ano"),
#         alt.Tooltip('revenue:Q', title="Receita", format="$,.2f")
#     ]
# ).interactive()

df4 = df.groupby(["year", "month"])["revenue"].sum().reset_index()

# Converter mês para string para que o eixo X o trate corretamente
df4["month"] = df4["month"].astype(str)

chart = alt.Chart(df4).mark_line(strokeWidth=3).encode(
    x=alt.X("month:N", title="Mês", sort=list(map(str, range(1, 13)))),
    y=alt.Y('revenue:Q', title="Receita"),
    color=alt.Color('year:N', title="Ano"),
    tooltip=[
        alt.Tooltip("month:N", title="Mês"),
        alt.Tooltip('year:N', title="Ano"),
        alt.Tooltip('revenue:Q', title="Receita", format="$,.2f")
    ]
).interactive()

st.altair_chart(chart, use_container_width=True)


# st.altair_chart(chart, use_container_width=True)





# st.write(ano_atual)
# st.write(ano_anterior)


# st.write(df_feriados)
st.write(df)

# st.write(df_feriados.dtypes)

























#import pathlib
# def load_css(file_path):
#     with open(file_path) as f:
#         st.html(f"<style>{f.read()}</style>")

# css_path = pathlib.Path("assets/styles.css")
# load_css(css_path)