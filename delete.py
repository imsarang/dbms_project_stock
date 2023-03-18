import streamlit as st
from database import userEmail,deleteUser,getUserInfo,getCompanyDetails,deleteCompany
def delete(table):
    if table=="user":
        email = userEmail()
        if st.button("remove account"):
            deleteUser(email)
            st.success("Successfully removed {}".format(email))
    if table=="company":
        email = userEmail()
        user_data = getUserInfo(email)
        #print()
        company = getCompanyDetails(user_data.iloc[0]['user_id'])
        for i in range(0,len(company)):
            st.subheader("Company : {}".format(company[i][1]))
            st.subheader("No of stocks in the company : {}".format(company[i][4]))
            if st.button('Remove Company',key=i):
                deleteCompany(company[i][1])
                st.success("Company {} Removed".format(company[i][1]))
            st.markdown('---')
            