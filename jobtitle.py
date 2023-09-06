import streamlit as st
import pymongo
from dateutil import parser
import time
import pandas as pd
from io import BytesIO
from xlsxwriter.workbook import Workbook
from datetime import datetime, timedelta
import re
import  streamlit_toggle as tog


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

Account = client['JobTitle_Account']

BankingFinance = client['JobTitle_BankingFinance']

Finance = client['JobTitle_Finance']

FoodSafety=client['JobTitle_FoodSafety']

Healthcare=client['JobTitle_Healthcare']

HumanResource = client['JobTitle_HumanResource']

Insurance = client['JobTitle_Insurance']

Pharmaceutical = client['JobTitle_Pharmaceutical']


def main():
    
    st.subheader("Update Job Title ")
    
    options = ["Select", "Account", "Banking&Finance", "Finance", "FoodSafety", "Healthcare", "HumanResource", "Insurance", "Pharmaceutical"]
    
    selected_option = st.selectbox("Select an option", options)
    

    if selected_option == "Account":
        db = Account
        
    elif selected_option == "Banking&Finance":
        db = BankingFinance
           
    elif selected_option == "Finance":
        db = Finance

    elif selected_option == "FoodSafety":
        db = FoodSafety
    
    elif selected_option == "Healthcare":
        db = Healthcare

    elif selected_option == "HumanResource":
        db = HumanResource
        
    elif selected_option == "Insurance":
        db = Insurance

    elif selected_option == "Pharmaceutical":
        db = Pharmaceutical
       
    
    existing_collections = db.list_collection_names()
    
    
    selected_collections = st.selectbox("Select JobTitle Collection:", existing_collections)
    
    st.write("------------------------------------------")
    
    selected_collection = db[selected_collections]
    
    jobtitles_list = selected_collection.distinct("JobTitle")
    
    df = pd.DataFrame(jobtitles_list)
    
    if st.button("Check exisiting Job Titles"):
    
        st.dataframe(df)
    
    tog_value = tog.st_toggle_switch(label="Switch input method", 
                key="Key1", 
                default_value=False, 
                label_after = False, 
                inactive_color = '#D3D3D3', 
                active_color="#11567f", 
                track_color="#29B5E8"
                )
    jobtitle=None
    if tog_value==True:
        
        jobtitle = st.text_input("Enter JobTitle:", value="")
    
    else:
        # Upload CSV file
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    st.write("------------------------------------------")
    
    if st.button("Add" , key = "add_button"):
        
        if jobtitle:
        
            document = {"JobTilte":jobtitle}
        
            try: 
        
                selected_collection.insert_one(document)
                                
                st.success(f"record inserted successfully")
        
            except:
        
                st.error("record could not be inserted successfully")

        elif uploaded_file:
        
                unique_jobtitles = set()
        
                existing_jobtitles = selected_collection.distinct("JobTitle")
        
                unique_jobtitles.update(existing_jobtitles)
        
                df = pd.read_csv(uploaded_file)
        
                st.write(df)
        
                # Prepare a list to store data to insert
                data_to_insert = []
        
                for index, row in df.iterrows():
        
                    jobtitle = row["JobTitle"]
        
                    if jobtitle in unique_jobtitles:
        
                        # st.warning(f"Duplicate email '{email}' skipped.")
                        continue

                    # If email is not in the set, add it to the seen_emails set
                    unique_jobtitles.add(jobtitle)
        
                    # Append data to the list for bulk insertion
                    data_to_insert.append({
                            "JobTitle": jobtitle 
                            })
        
                # Insert data into the desired collection using insert_many
                try:
        
                    selected_collection.insert_many(data_to_insert)
        
                    st.success(f"Inserted {len(data_to_insert)} emails successfully.")
        
                except Exception as e:
        
                    st.error(f"Error inserting data: {e}")

        time.sleep(2)
        
        st.experimental_rerun()  # Refresh the app






