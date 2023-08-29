import streamlit as st
import pymongo
from dateutil import parser
import time
import pandas as pd
from io import BytesIO
from xlsxwriter.workbook import Workbook
from datetime import datetime, timedelta


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
    st.subheader("Generate CSV")
    options = ["Select", "Account", "Banking&Finance", "Finance", "FoodSafety", "Healthcare", "HumanResource", "Insurance", "Pharmaceutical"]
    selected_option = st.selectbox("Select an option", options)
    
    if selected_option == "Account":
        collection = Account
        collection_archieves = Account_archieves
        
    elif selected_option == "Banking&Finance":
        collection = BankingFinance
        collection_archieves = BankingFinance_archieves   
    
    elif selected_option == "Finance":
        collection = Finance
        collection_archieves = Finance_archieves
    
    elif selected_option == "FoodSafety":
        collection = FoodSafety
        collection_archieves = FoodSafety_archieves
    
    elif selected_option == "Healthcare":
        collection = Healthcare
        collection_archieves = Healthcare_archieves
        
    elif selected_option == "HumanResource":
        collection = HumanResource
        collection_archieves = HumanResource_archieves
        
    elif selected_option == "Insurance":
        collection = Insurance
        collection_archieves = Insurance_archieves
    
    elif selected_option == "Pharmaceutical":
        collection = Pharmaceutical
        collection_archieves = Pharmaceutical_archieves
    
        
    st.write(f"You selected: {selected_option}")
    
    generate_button = st.button("Click to generate the view")
    st.write("**************************************************************")
    projection = {
    "Date": 1,
    "Email": 1,
    "JobTitle": 1,
    "Department": 1,
    "Industry": 1,
    "_id": 0  # Exclude the default _id field
}
    if generate_button:
        # Calculate the date range for the last 7 days
        end_date = datetime.now()  # Current date and time
        start_date = end_date - timedelta(days=10)  # 7 days ago

        # Query to retrieve documents within the last 7 days
        query = {"Date": {
        "$gte": start_date.strftime('%Y-%m-%d %H:%M:%S'),
        "$lt": end_date.strftime('%Y-%m-%d %H:%M:%S')}
        }
        # Fetch documents using the query

        results = collection.find(query, projection)
        # Create a DataFrame from the query results
        df = pd.DataFrame(results)
        st.write(df)

        # Save DataFrame to a CSV file
        csv_filename = 'query_results.csv'
        df.to_csv(csv_filename, index=False)

        # Provide a link to download the CSV file
        st.markdown(f"Download [query_results.csv](./{csv_filename})", unsafe_allow_html=True)
        


