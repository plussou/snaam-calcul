import streamlit as st

from streamlit_option_menu import option_menu
import pandas as pd

# Function to generate nudge
def select_cht(lg,ep,pose):
    gamme_cht=pd.read_csv("data/gamme_cht.csv",dtype={'h_plancher':int})
    sel_0=gamme_cht[gamme_cht['h_plancher']==ep]
    sel_1=sel_0[sel_0['portee_min']<lg]
    selected=sel_1[sel_1['portee_max']>=lg].drop(labels=['portee_min','portee_max','h_plancher'],axis=1)
    if pose=="Poutrelle/Mur":
        selected['code']=selected['code']+' (M)'
    selected.rename({'p_ser':'charge admissible [kN/ml]'},axis=1,inplace=True)
    selected.set_index('code',inplace=True)
    return selected

def select_pal(lg,ep):
    gamme_pal=pd.read_csv("data/gamme_pal.csv")
    sel_0=gamme_pal[gamme_pal['portee_min']<lg]
    sel_1=sel_0[sel_0['portee_max']>=lg].drop(labels=['portee_min','portee_max'],axis=1)
    sel_2=sel_1[sel_1['h_poutre']==ep]
    selected = sel_2.rename({'p_ser':'charge admissible [kN/ml]',\
                     'h_poutre':'hauteur poutre [cm]'},axis=1)
    selected.set_index('code',inplace=True)
    return selected

with st.sidebar:
    st.image('media/logo_snaam.png',width=300)
    selected = option_menu(
        menu_title = "Menu",
        options = ["PAL","CHT"],
        menu_icon = "calculator"
        )

if selected == "PAL":
    st.title("Poutre à longueur")
    st.image('media/vue_enlong.jpg',width=500)
    lg = st.slider("Portée ", min_value=200, max_value=700,step=50)
    ep = st.number_input("Hauteur poutre", min_value=20, max_value=55, step=5)
    if st.button("Déterminer mon produit"):
        st.dataframe(select_pal(lg,ep))

if selected == "CHT":
    st.title("Chevêtre à longueur")
    pose = st.selectbox("Mode de pose",["Poutrelle/Poutrelle", "Poutrelle/Mur"])
    lg = st.number_input("Dimension trémie", min_value=60, max_value=420,step=10)
    ep = st.number_input("Epaisseur plancher", min_value=16, max_value=24, step=4)
    if st.button("Déterminer mon produit"):
        st.dataframe(select_cht(lg,ep,pose))
