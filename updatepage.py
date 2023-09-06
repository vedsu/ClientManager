import streamlit as st
import pymongo
from dateutil import parser
import time
import pandas as pd
from io import BytesIO
from xlsxwriter.workbook import Workbook
import deletepage

#Database connections
@st.cache_resource
def init_connection():
   
    try:
    
        db_username = st.secrets.db_username
        db_password = st.secrets.db_password

        mongo_uri_template = "mongodb+srv://{username}:{password}@emailreader.elzbauk.mongodb.net/"
        mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)

        client = pymongo.MongoClient(mongo_uri)
        return client
    
    except:
    
        st.write("Connection Could not be Established with database")

#  Database
client = init_connection()
db= client['ClientDatabase']

Account = db["Account"]
Account_archieves = db['Account_archieves']

BankingFinance = db["Banking&Finance"]
BankingFinance_archieves = db['Banking&Finance_archieves']

Finance = db['Finance']
Finance_archieves=db['Finance_archieves']

FoodSafety=db["FoodSafety"]
FoodSafety_archieves=db["FoodSafety_archieves"]

Healthcare=db['Healthcare']
Healthcare_archieves=db['Healthcare_archieves']

HumanResource = db["HumanResource"]
HumanResource_archieves = db['HumanResource_archieves']

Insurance = db['Insurance']
Insurance_archieves= db['Insurance_archieves']

Pharmaceutical = db['Pharmaceutical']
Pharmaceutical_archieves = db['Pharmaceutical_archieves']


def main():

    st.subheader("Update Client Database")

    options = ["Select", "Account", "Banking&Finance", "Finance", "FoodSafety", "Healthcare", "HumanResource", "Insurance", "Pharmaceutical"]

    selected_option = st.selectbox("Select an option", options)
    
    if selected_option == "Account":

        collection = Account
        
    elif selected_option == "Banking&Finance":

        collection = BankingFinance
           
    elif selected_option == "Finance":

        collection = Finance
    
    elif selected_option == "FoodSafety":

        collection = FoodSafety
            
    elif selected_option == "Healthcare":
        collection = Healthcare
            
    elif selected_option == "HumanResource":
        
        collection = HumanResource
            
    elif selected_option == "Insurance":
        
        collection = Insurance
        
    elif selected_option == "Pharmaceutical":
        
        collection = Pharmaceutical
            
    st.write(f"You selected: {selected_option}")
    
    # Upload CSV file
    
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file:
    
        df = pd.read_csv(uploaded_file)
    
        st.write(df)
    
        # Insert CSV data into the database
    
        if st.button("Update" , key = "update_button"):
    
            st.warning(f"uploading files to {selected_option} please wait")
    
            for index, row in df.iterrows():
    
                    existing_document = collection.find_one({"Email": row["Email"]})
    
                    if existing_document is None:
    
                        data_to_insert = {
                "FName": row["FName"],
                "LName": row["LName"],
                "JobTitle": row["JobTitle"],
                "Department": row["Department"],
                "Industry": row["Industry"],
                "Company": row["Company"],
                "Email": row["Email"],
                "City": row["City"],
                "State": row["State"],
                "Phone": row["Phone"],
                "EmpID": row["EmpID"],
                "Date": row["Date"],
                "Medium": row["Medium"],
                "Status": row["Status"],
                "TimeZone": row["TimeZone"]

                }
    
                    # Insert data into the desired collection
    
                        try:
    
                            collection.insert_one(data_to_insert)
    
                        except:
    
                            st.error("please check the csv file again")

            st.success("Uploaded successfully")

            time.sleep(1)
    
            st.experimental_rerun()  # Refresh the app