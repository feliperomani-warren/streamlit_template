import streamlit as st

# --- PAGE SETUP ---
pagina_inicial = st.Page(
    "pages/Receitas_por_Mesa_e_Ativo.py",
    title="Receitas por Mesa e Ativo",
    icon=":material/attach_money:",
    default=True,
)

pagina_resultados = st.Page(
    "pages/Acompanhamento_Metas.py",
    title="Acompanhamento Metas",
    icon=":material/target:",
)

# pagina_login = st.Page(
#     "pages/login.py",
#     title="Login",
#     icon=":material/contacts:",
# )

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation({
    "Institucional": [pagina_inicial, pagina_resultados],
    # "Informações": [pagina_login],
})


# --- RUN NAVIGATION ---
pg.run()