import streamlit as st
from database import add_user_account
from database import add_company
def create(table):
    if table == 'user':
        st.subheader("Enter User Details")
        col1, col2 = st.columns(2)
        with col1:
            # user_id = st.text_input("user_id:")
            name = st.text_input("Name:")
            # lname =  st.text_input("lname:")
            # dob =  st.text_input("dob:")
            # phone =  st.text_input("phone:")
            email = st.text_input("Email:")
            works_in = st.text_input("Works In:")

        with col2:
            gender = st.text_input("Gender:")
            password = st.text_input("Password:")
            age = st.text_input("Age:")
            # country = st.text_input("country:")
            # city = st.text_input("city:")
            # pincode= st.text_input("pincode:")
            # bank_name = st.text_input("bank_name:")
        st.subheader("Bank details")
        balance = st.text_input('balance')
        bank_name = st.text_input('bank name')

        if st.button("Add data"):
            add_user_account(name ,email ,password,works_in,gender,age,balance,bank_name)
            st.success("Successfully registered : {}".format(email))
        

    elif table == 'company':
        st.subheader("Enter User Details")
        col1, col2 = st.columns(2)
        with col1:
            # user_id = st.text_input("user_id:")
            name = st.text_input("Company Name:")
            price = st.text_input("Price of One Stock:")

        with col2:
           no_of_stocks = st.text_input("Number of stocks")
            # country = st.text_input("country:")
            # city = st.text_input("city:")
            # pincode= st.text_input("pincode:")
            # bank_name = st.text_input("bank_name:") 
        if st.button("Add data"):
            add_company(name ,no_of_stocks,price)
            st.success("Successfully registered : {}".format(name))

