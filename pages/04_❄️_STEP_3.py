import streamlit as st
import plotly.graph_objects as go
import numpy as np
from data import *

st.set_page_config(layout="wide")
@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache
def gen_spectre(dam,t_max):
    T3 = np.arange(0.01,2,0.05)
    T4 = np.arange(2,t_max,0.2)
    T = np.hstack((T3,T4))
    Data.df_nw = pd.DataFrame()
    Data.acc_signal_2.gen_response_spectrum(response_times=T,xi=dam/100)
    Data.df_nw["Period (s)"] = Data.acc_signal_2.response_times
    Data.df_nw["Acceleration (cm/s2)"] = Data.acc_signal_2.s_a
    Data.df_nw["Velocity (cm/s)"] = Data.acc_signal_2.s_v
    Data.df_nw["Displacement (cm)"] = Data.acc_signal_2.s_d



st.markdown("# ELASTIC RESPONSE SPECTRA")
with st.expander("OPTIONS"):
    col1,col2,col3 = st.columns(3)

    try:
        dam = col1.number_input("Damping (%)",value = Data.dam)
        t_max = col2.number_input("Max.Period (s)",value=Data.T_max)
    except:
        dam = col1.number_input("Damping (%)",value = 5)
        t_max = col2.number_input("Max.Period (s)",value=5)
    Data.dam = dam
    Data.T_max = t_max

    xaxis = col1.selectbox("X-Axis",["Period (s)","Displacement (cm)"])
    yaxis = col2.selectbox("Y-Axis",["Acceleration (cm/s2)","Velocity (cm/s)","Displacement (cm)"])
    app = col1.button("Apply")

if app:
    gen_spectre(Data.dam,Data.T_max)
    st.experimental_rerun()

if Data.df_nw is not None:
    fig = go.Figure()
    fig.add_scatter(x=Data.df_nw[xaxis],y=Data.df_nw[yaxis],line=dict(color="blue",width=1))
    if xaxis == "Period (s)":
        fig.update_xaxes(title_text=xaxis)
    else: fig.update_xaxes(title_text=xaxis)

    fig.update_yaxes(title_text=yaxis)
    fig.update_layout(
        height=1000,autosize=False,
        showlegend=False
    )
    st.plotly_chart(fig,use_container_width=True)

    st.write(Data.df_nw)

    csv = convert_df(Data.df_nw)
    dw = st.download_button(
        label = "Download data as CSV",
        data = csv,
        file_name = "spectra_data.csv",
        mime = 'text/csv'
    )
