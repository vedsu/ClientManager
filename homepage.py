import streamlit as st
import pymongo
from dateutil import parser
import time
import pandas as pd
from io import BytesIO
from xlsxwriter.workbook import Workbook
import hardbounce
import updatepage
import generatecsv
import unsubscribe
import jobtitle

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
    
    # Radio buttons to navigate between pages
    
    st.sidebar.subheader("Instruction to use")
    st.sidebar.text("1. Go to Update Client Data select the industry and upload their CSV file.")
    st.sidebar.text("2. Go to Update Hardbounce upload their CSV file. ")
    st.sidebar.text("3. Go to Update Unsubscribe upload their CSV file. ")
    st.sidebar.text("4. Go to Update Jobtitle upload their CSV file. ")
    st.sidebar.text("5. Generate CSV file select the industry and Download the updated CSV file. ")
    st.sidebar.write("----------------------------------")

    
    st.sidebar.subheader("Navigation Menu")
    
    navigation = st.sidebar.radio("Click to Navigate", ("1. Update Client data", "2. Update Hardbounce", "3. Update Unsubscribe", "4. Update Jobtitle", "5. Generate CSV file"))
    
    st.sidebar.write("----------------------------------")
    
    if navigation=="1. Update Client data":  
    
        updatepage.main()
    
    elif navigation=="2. Update Hardbounce":
    
        hardbounce.main()
    
    elif navigation=="3. Update Unsubscribe":
    
        unsubscribe.main()
    
    elif navigation=="4. Update Jobtitle":
    
        jobtitle.main()
    
    elif navigation=="5. Generate CSV file":
    
        generatecsv.main()



                    