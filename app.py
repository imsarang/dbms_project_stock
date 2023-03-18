import mysql.connector
import streamlit as st

from database import create_table,getCompanyWithMaxNoOfStocks,getCompanyWithMaxStockValue,getCompanyWithMinStocks
from create import create
from update import update
from delete import delete
from auth import auth
from auth import login_auth
from auth import logout_auth
from joins import joins
from chart import chart
mydb = mysql.connector.connect(
host="localhost",
user="root",
password=""
)
c = mydb.cursor()
c.execute("CREATE DATABASE if not exists stock_market_management")

def main():
    st.title("Stock Market Management")
    create_table()
    max_com=getCompanyWithMaxNoOfStocks()
    st.subheader("Company with max number of stocks : {}".format(max_com[0][1]))
    st.subheader("Company with min number of stocks : {}".format(getCompanyWithMinStocks()[0][1]))
    # st.subheader("Company with max stock value : {}".format(getCompanyWithMaxStockValue()[0][1]))
    # st.markdown('---')
    sidebar=['CRUD','AUTH','OTHERS','CHART']
    sidebar_choice = st.sidebar.selectbox("MAIN",sidebar)
    if sidebar_choice==sidebar[0]:

        menu=["Add User","Create Company","Update User","Update Company","Remove User","Remove Company"]
        choice = st.sidebar.selectbox("Menu",menu)
        if choice==menu[0]:
            table="user"
            create(table)
        elif choice==menu[1]:
            table="company"
            create(table)
        elif choice==menu[2]:
            table="user"
            update(table)
        elif choice==menu[3]:
            table="company"
            update(table)
        elif choice==menu[4]:
            table="user"
            delete(table)
        elif choice==menu[5]:
            table="company"
            delete(table)
    elif sidebar_choice==sidebar[1]:
        auth()
        # pass
    elif sidebar_choice==sidebar[2]:
        actions = ["Buy","Sell","Profile","Stocks Owned","Employees","get_all","SQL Query"]
        choice_actions = st.sidebar.selectbox("Actions",actions)
        if choice_actions == actions[0]:
            joins(actions[0])
        elif choice_actions == actions[1]:
            joins(actions[1])
        elif choice_actions == actions[2]:
            joins(actions[2])
        elif choice_actions == actions[3]:
            joins(actions[3])
        elif choice_actions == actions[4]:
            joins(actions[4])
        elif choice_actions == actions[5]:
            joins(actions[5])
        elif choice_actions == actions[6]:
            joins(actions[6])
    else:
        chart()
    # table_names = ['bankdetails','company','invoice','stock','user']
    # table=st.sidebar.selectbox("table", table_names)
    
    

    
        

if __name__ == "__main__":
    main()