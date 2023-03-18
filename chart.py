from database import getPieChart
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import plotly.express as px

def chart():
    data=getPieChart()
    df=pd.DataFrame(data,columns=['stocks','company'])
    labels=df.iloc[1]['company']
    size=df.iloc[0]['stocks']
    fig1, ax1 = plt.subplots()
    p1 = px.pie(df,names='company',values='stocks')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # st.pyplot(fig1)
    st.plotly_chart(p1)
    p2 = px.bar(df,x='company',y='stocks')
    st.plotly_chart(p2)
    
