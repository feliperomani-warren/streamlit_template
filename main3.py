import pandas as pd
import streamlit as st

nome_arquivo = "mkt_share_corretoras_anual.xlsx"
xls = pd.ExcelFile(nome_arquivo)

nomes_chaves = ["DI1", "DOL", "FRC", "DAP", "mini DOL", "mini IND", "FRP0", "BOVESPA TOTAL", "BM&F TOTAL"]
meses = ("Jan", "Fev", "Mar", "Abr", "Mai", "Jun","Jul", "Ago", "Set", "Out", "Nov", "Dez")
anos_abas = ("25")
abas_filtradas = [sheet for sheet in xls.sheet_names if sheet.endswith(anos_abas)]

df2 = pd.read_excel(nome_arquivo, sheet_name="df")


dfs_dict = {}
for aba in abas_filtradas:
    
    df = pd.read_excel(nome_arquivo, sheet_name=aba, header=3)
    
    assert len(nomes_chaves) == (df.shape[1] // 5), "Erro: Número de chaves não corresponde ao número de DataFrames esperados!"

    for i, nome in enumerate(nomes_chaves):
        df_temp = df.iloc[:, i*5:(i+1)*5].copy()  # Pegando 5 colunas de cada vez
        df_temp.columns = [col.split(".")[0] for col in df_temp.columns]
        
        df_temp["Ativo"] = nome
        df_temp["Mês"] = aba
        df_temp["Ano"] = 2025

        if nome not in dfs_dict:
            dfs_dict[nome] = []

        dfs_dict[nome].append(df_temp)

df_final = pd.concat([pd.concat(dfs_dict[key], ignore_index=True) for key in dfs_dict], ignore_index=True)
# df_final = pd.concat([df_final, df2])
df_final = df_final.dropna(subset=["Corretora"])

df1 = df_final.groupby(["Mês", "Ativo"])["Nº Contratos"].sum().reset_index()
# st.bar_chart(df1, x="Mês" ,y="Nº Contratos", color="Ativo")#, color="Ativo"

# mes = st.selectbox("Selecione o Mês", abas_filtradas, index=len(abas_filtradas)-1)
# mercado = st.selectbox("Selecione o Ativo", df_final["Ativo"].unique())

st.write(dfs_dict)
st.write(df_final)