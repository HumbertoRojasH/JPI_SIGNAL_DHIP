import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from data import *

st.set_page_config(layout="wide")

@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

st.markdown("# BASELINE CORRECTION AND FILTERING")

with st.expander("OPTIONS"):
    col1,col2,col3 = st.columns(3)
    col1.write("")
    bl = col1.checkbox("Baseline Correction")
    fil = col1.checkbox("Filtering")
    ud = col1.checkbox("Plot Unconrrected Data")
    col1.write("")
    ap = col1.button("Apply")

    col2.write("Baseline Correction")
    col3.write("Filtering")

    try:
        type = col2.radio("Polynomial Type",["Linear","Quadratic","Cubic"],index=["Linear","Quadratic","Cubic"].index(Data.type))
        frq1 = col3.number_input("Freq 1 (Hz)", value= Data.frq1)
        frq2 = col3.number_input("Freq 2 (Hz)", value= Data.frq2)
    except:
        type = col2.radio("Polynomial Type",["Linear","Quadratic","Cubic"])
        frq1 = col3.number_input("Freq 1 (Hz)", value= 0.1)
        frq2 = col3.number_input("Freq 2 (Hz)", value= 50)
    
    Data.type = type
    Data.frq1 = frq1
    Data.frq2 = frq2
    Data.bl = bl
    Data.fil = fil

    try:
        fig = go.Figure()
        fig.add_scatter(x=Data.acc_signal.fa_frequencies,y=abs(Data.acc_signal.fa_spectrum),line=dict(color="gray",width=1),name="Fourier Spectrum")
        fig.add_scatter(x=Data.acc_signal.smooth_fa_frequencies,y=abs(Data.acc_signal.smooth_fa_spectrum),line=dict(color="blue",width=1),name="Smoothed Fourier Spectrum (Konno and Ohmachi)")
        fig.update_xaxes(title_text="Frecuency (Hz)",type="log")
        fig.update_yaxes(title_text="Fourier Amplitude",type="log")
        fig.update_layout(
            height=700,autosize=False,
            showlegend=True, legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        st.plotly_chart(fig,use_container_width=True)
    except:pass

if ap:
    Data.baseline_filtering(Data)

    st.write("## Corrected Data:")

    fig=make_subplots(rows=3,cols=1,shared_xaxes=True, vertical_spacing=0.05)

    if ud:
        fig.add_scatter(x=Data.df["Time"],y=Data.df["Acc"],line=dict(color="gray",width=1),row=1,col=1)
        fig.add_scatter(x=Data.df["Time"],y=Data.df["Vel"],line=dict(color="gray",width=1),row=2,col=1)
        fig.add_scatter(x=Data.df["Time"],y=Data.df["Dis"],line=dict(color="gray",width=1),row=3,col=1)

    fig.add_scatter(x=Data.df_c["Time"],y=Data.df_c["Acc"],line=dict(color="blue",width=1),row=1,col=1)
    fig.add_scatter(x=Data.df_c["Time"],y=Data.df_c["Vel"],line=dict(color="blue",width=1),row=2,col=1)
    fig.add_scatter(x=Data.df_c["Time"],y=Data.df_c["Dis"],line=dict(color="blue",width=1),row=3,col=1)

    fig.update_yaxes(title_text="Acceleration (cm/s2)",row=1,col=1)
    fig.update_yaxes(title_text="Velocity (cm/s)",row=2,col=1)
    fig.update_yaxes(title_text="Displacement (cm)",row=3,col=1)

    fig.update_xaxes(title_text="Time (s)",row=3,col=1)

    fig.update_layout(
        height=900,autosize=False,
        showlegend=False
    )
    st.plotly_chart(fig,use_container_width=True)

    st.write(Data.df_c)

    csv = convert_df(Data.df_c)
    dw = st.download_button(
        label = "Download data as CSV",
        data = csv,
        file_name = "corrected_data.csv",
        mime = 'text/csv'
    )
