import streamlit as st
from database import userEmail,getStocksOwnedByUser,getCompany,employeeCompany,getManagerData,getWorksIn,getUserInfo,checkToOwn,companyByName,union,intersect,setExcept,union_all
import pandas as pd
from update import trade,sellStocks
from queries import execute_query

def joins(section):
    if section=="Buy":
        trade()
    elif section=="Sell":
        sellStocks()
    elif section=="Profile":
        st.header("USER PROFILE")
        email = userEmail()
        user_df = getUserInfo(email)
        st.subheader('name : ')
        st.text(user_df.iloc[0]['name'])
        st.subheader('email : ')
        st.text(user_df.iloc[0]['email'])
        st.subheader('works_in : ')
        st.text(user_df.iloc[0]['works_in'])
        res_text = checkToOwn(email)
        res_text = res_text[0][1]
        st.text(res_text)

    elif section=="Stocks Owned":

        st.header("STOCKS OWNED")
        email = userEmail()
        join_data = getStocksOwnedByUser(email)
        for i in range(0,len(join_data)):
            # if(len(join_data[i])>0):
                name = companyByName(join_data[i][13])
                print(name)
                # name = name[0][1]
                company_name = st.subheader('Stock name : {}'.format(name[0][1]))
                stocks_owned = st.subheader('Number of stocks owned : {}'.format(join_data[i][14]))
                st.markdown('---')
    elif section == "Employees":
        st.header("DATAFRAME OF ALL YOUR EMPLOYEES : ")
        email=userEmail()
        company_name=getWorksIn(email)
        result=employeeCompany(company_name)
        df= pd.DataFrame(result,columns=['company_id','company_name','manager_id','stock_id','no_of_stocks','user_id','name','email','password','age','works_in','gender'])
        with st.expander("View all employees  "):
            st.dataframe(df)
        
        result_union = union()
        result_inter = intersect()
        result_except = setExcept()
        result_all = union_all()

        union_df = pd.DataFrame(result_union,columns=['user_id'])
        intersect_df = pd.DataFrame(result_inter,columns=['user_id'])
        except_df =pd.DataFrame(result_except,columns=['user_id'])
        union_all_df = pd.DataFrame(result_all,columns=['company','manager_id'])
        st.subheader('Union of users and managers')
        st.dataframe(union_df)

        st.subheader('Intersection of users and managers')
        st.dataframe(intersect_df)

        st.subheader('All users who donot own a company')
        st.dataframe(except_df)

        st.subheader('Managers and their company')
        st.dataframe(union_all_df)
        
    elif section == "get_all_employees":
        st.header
    elif section=="SQL Query":
        st.subheader('Enter Query')
        execute_query()
        pass