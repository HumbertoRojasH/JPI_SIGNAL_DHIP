import streamlit as st
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import  plotly.graph_objects as go
from eqsig.single import AccSignal
from data import *

st.set_page_config(layout="wide")

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

st.markdown("# INPUT DATA")
st.sidebar.markdown("# INPUT DATA")

file = st.file_uploader("Upload a file")

if file is not None:
    Data.file = file
    Data.acc = np.genfromtxt(Data.file)

if Data.file is not None:

    try:
        hz = st.sidebar.text_input("SAMPLING FREQUENCY (Hz)",value=str(int(1/Data.dt)))
        n = st.sidebar.text_input("NUMBER OF SAMPLES", value=str(Data.n))
        fac = st.sidebar.text_input("FACTOR CONVERTION TO (cms/s2)",value=str(Data.fac))
    except:
        hz = st.sidebar.text_input("SAMPLING FREQUENCY (Hz)",value=str(200))
        n = st.sidebar.text_input("NUMBER OF SAMPLES", value=str(len(Data.acc)))
        fac = st.sidebar.text_input("FACTOR CONVERTION TO (cms/s2)",value=str(1))
    
    Data.dt = 1/float(hz)
    Data.n = int(n)
    Data.fac = float(fac)

    Data.acc_signal = AccSignal(Data.acc[0:Data.n]*Data.fac,Data.dt,smooth_freq_range=(0.01,(1/Data.dt)/2))
    Data.acc_signal.generate_displacement_and_velocity_series()
    Data.df = pd.DataFrame()
    Data.df["Time"] = Data.acc_signal.time
    Data.df["Acc"] = Data.acc_signal.values
    Data.df["Vel"] = Data.acc_signal.velocity
    Data.df["Dis"] = Data.acc_signal.displacement

    st.write("## Unconrrected data:")

    fig = make_subplots(rows=3,cols=1,shared_xaxes=True, vertical_spacing=0.05)
    fig.add_scatter(x=Data.df["Time"],y=Data.df["Acc"],line=dict(color="blue",width=1),row=1,col=1)
    fig.add_scatter(x=Data.df["Time"],y=Data.df["Vel"],line=dict(color="blue",width=1),row=2,col=1)
    fig.add_scatter(x=Data.df["Time"],y=Data.df["Dis"],line=dict(color="blue",width=1),row=3,col=1)

    fig.update_yaxes(title_text="Acceleration (cm/s2)",row=1,col=1)
    fig.update_yaxes(title_text="Velocity (cm/s)",row=2,col=1)
    fig.update_yaxes(title_text="Displacement (cm)",row=3,col=1)

    fig.update_xaxes(title_text="Time (s)",row=3,col=1)

    fig.update_layout(
        height=900,autosize=False,
        showlegend=False
    )
    st.plotly_chart(fig,use_container_width=True)

    st.write(Data.df)

    csv = convert_df(Data.df)
    dw = st.download_button(
        label = "Download data as CSV",
        data = csv,
        file_name = "uncorrected_data.csv",
        mime = 'text/csv'
    )