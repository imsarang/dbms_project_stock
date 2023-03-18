import streamlit as st
from database import userEmail,getUserInfo,updateUser,updateCompany,getCompanyDetails,getStockDetails,getCompanies,getStock,getCompaniesOwned,getBankDetails,getManagerData,updateStockCompanies,stockCompanyOwned,companyByName,updateSellStock
import mysql.connector
import pandas as pd

mydb = mysql.connector.connect(
    host="localhost", user="root", password="",
    database="stock_market_management"
)
c = mydb.cursor()


def update(table):
    if(table=="user"):
        email = userEmail()
        user_df = getUserInfo(email)
        new_name = st.text_input("username : ",user_df.iloc[0]['name'])
        new_password = st.text_input("password : ",user_df.iloc[0]['password'])
        new_works_in = st.text_input("works in : ",user_df.iloc[0]['works_in'])
        new_age = st.text_input("age : ",user_df.iloc[0]['age'])
        if st.button("Update User Account"):
                updateUser(new_name,new_password,new_works_in,new_age,email)
                st.success("Successfully updated:{}".format(email))
    
    elif(table=="company"):
        email = userEmail()
        user_df = getUserInfo(email)
        user_id = int(user_df.iloc[0]['user_id'])
        company_data = getCompanyDetails(user_id)

        for i in range(0,len(company_data)):
            company_id = company_data[i][0]
            stock_id = company_data[i][3]
            stock_data = getStockDetails(stock_id)
            # print(stock_data)
            stock_price = stock_data[0][3]
            old_name = company_data[i][1]
            new_name = st.text_input("company name : ",company_data[i][1],key=i)
            new_buying_price = st.text_input("Stock Buying Price : ",stock_price,key=company_data[i][1]+str(0)+str(stock_id)+str(company_id))
            if st.button("Update company details",key=company_data[i][1]+str(company_id)):
                updateCompany(new_name,new_buying_price,email,company_id,stock_id,old_name)
                st.success("Successfully updated :{}".format(company_data[i][1]))
        

def trade():
    email = userEmail()
    user_df = getUserInfo(email)
    user_id = user_df.iloc[0]['user_id']
    company = getCompanies(user_id)
    bank = getBankDetails(email)
    st.subheader("Balance : {}".format(bank[0][1]))
    st.markdown('---')

    for i in range(0,len(company)):
        stock_data = getStock(company[i][0])
        # manager = getManagerData(company[i][1])
        st.subheader('Company Name : {}'.format(company[i][1]))
        # st.subheader('Company Owner : {}'.format(manager[0][1]))
        st.subheader('Buying Price : {}'.format(stock_data[i][4])) 
        # print(stock_data[i][4])
        st.subheader('Stocks Available : {}'.format(company[i][4]))
        num_input = st.text_input('Stocks to purchase : ',key=i)
        if st.button('Buy',key=100+(i*i)+1):
            # if int(num_input) > int(company[i][4]):
                purchase = int(num_input)*stock_data[i][3]
                updateStockCompanies(company[i][0],stock_data[i][0],user_id,company[i][4],int(num_input),bank[0][1],purchase)
                st.success('Purchase Successful')
            # else:
                # st.error('Num of stocks cannot be greater than available')    
        st.markdown('---')
    
def sellStocks():
    email = userEmail()
    user_df = getUserInfo(email)
    user_id = user_df.iloc[0]['user_id']
    bank = getBankDetails(email)
    # company = 
    stocks_own = stockCompanyOwned(user_id)
    bank = getBankDetails(email)
    st.subheader("Balance : {}".format(bank[0][1]))
    st.markdown('---')
    for i in range(0,len(stocks_own)):
        company = companyByName(stocks_own[i][6])
        st.subheader('Stock Name : {}'.format(stocks_own[i][6]))
        st.subheader('Selling Price : {}'.format(stocks_own[i][4]))
        st.subheader('Number of Stocks owned : {}'.format(stocks_own[i][8]))
        new_num = st.text_input('Number of stocks you want to sell : ',key=i)
        if st.button('Sell',key=100+i):
            sell = stocks_own[i][4] * int(new_num)
            updateSellStock(stocks_own[i][6],user_id,stocks_own[i][8],int(new_num),bank[0][1],sell,company[0][4],stocks_own[i][4],company[0][0],stocks_own[i][0])
            st.success("Stocks sold")

        st.markdown('---')