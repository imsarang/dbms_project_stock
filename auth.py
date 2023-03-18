import streamlit as st
import mysql.connector
from database import add_login_db
# from database import user
from database import deleteLoginRecord
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    database="stock_market_management"
)
c = mydb.cursor()
def auth():
    # if already in login db:
    auth = ["login","logout"]
    choice = st.sidebar.selectbox("Auth",auth)
    # c.execute("select * from login")
    # login_data = c.fetchall()
    # if(login_data):
    #     logout_auth(login_data)
    #     return True
    # else: 
    #     login_auth()
    #     return False
    if choice==auth[0]:
        login_auth()
    else:
        c.execute("select * from login")
        login_data = c.fetchall()
        logout_auth(login_data)
    
def login_auth():
    st.subheader("Login")
    email = st.text_input("Registered Email ID")
    password  = st.text_input("Password")
    if st.button("Login"):
        add_login_db(email ,password)
        # user(email)
        st.success("Successfully Logged In : {}".format(email))

def logout_auth(login_data):
    df = pd.DataFrame(login_data,columns=['login_id','email','password'])
    print(df)
    deleteLoginRecord(df['email'])


