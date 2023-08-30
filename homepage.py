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
    st.sidebar.text("1. Go to Update Client Data select the department and upload their respective CSV file.")
    st.sidebar.text("2. Go to Update Hardbounce/Unsubscribe select the option & upload CSV their file. ")
    st.sidebar.text("3. Go to Delete Client data & directly upload CSV harbounce, unsubscribe file. ")
    st.sidebar.text("4. Generate CSV file and Download the updated CSV file. ")
    st.sidebar.write("----------------------------------")

    
    
    
    
    st.sidebar.subheader("Navigation Menu")
    navigation = st.sidebar.radio("Click to Navigate", ("1. Update Client data", "2. Update Hardbounce", "3. Update Unsubscribe",   "4. Generate CSV file"))
    st.sidebar.write("----------------------------------")
    if navigation=="3. Update Unsubscribe":
        unsubscribe.main()
        # with st.container():
        #     st.write("-------------------------------------------------------------")
        #     st.warning("Delete clients")
        #     st.write("-------------------------------------------------------------")
        #     col1, col2 = st.columns(2)
        #     with col1:
        #         # with st.expander("1. Delete with email"):
        #                 # Dropdown select box
        #                 email = st.text_input("Email:", value="")
        #                 options = ["Select", "Account", "Banking&Finance", "Finance", "FoodSafety", "Healthcare", "HumanResource", "Insurance", "Pharmaceutical"]
        #                 selected_option = st.selectbox("Select an option", options)
                        
        #                 if selected_option == "Account":
        #                     collection = Account
        #                     collection_archieves = Account_archieves
                            
        #                 elif selected_option == "Banking&Finance":
        #                     collection = BankingFinance
        #                     collection_archieves = BankingFinance_archieves   
                        
        #                 elif selected_option == "Finance":
        #                     collection = Finance
        #                     collection_archieves = Finance_archieves
                        
        #                 elif selected_option == "FoodSafety":
        #                     collection = FoodSafety
        #                     collection_archieves = FoodSafety_archieves
                        
        #                 elif selected_option == "Healthcare":
        #                     collection = Healthcare
        #                     collection_archieves = Healthcare_archieves
                            
        #                 elif selected_option == "HumanResource":
        #                     collection = HumanResource
        #                     collection_archieves = HumanResource_archieves
                            
        #                 elif selected_option == "Insurance":
        #                     collection = Insurance
        #                     collection_archieves = Insurance_archieves
                        
        #                 elif selected_option == "Pharmaceutical":
        #                     collection = Pharmaceutical
        #                     collection_archieves = Pharmaceutical_archieves
                        
                            
                            
                            
                            
        #                 st.write(f"You selected: {selected_option}")
        #                 # Delete button
        #                 if st.button("Delete") and selected_option != "Select":
        #                     query = {"Email":email}
        #                     try: 
        #                         results = collection.find(query)
        #                         count = 0
        #                         for result in results:
        #                             collection_archieves.insert_one(result)
        #                             count += 1
        #                         if count > 0:
        #                             collection.delete_many(query)
        #                             st.success(f"Deleted {count} records successfully")
        #                         else:
        #                             st.warning("No records found with the given email")
        #                         time.sleep(1)
        #                     except:
        #                         st.error("email id not found")
        #                         time.sleep(1)
        
        #                     st.experimental_rerun()
                            

        #                     # Perform the deletion or processing here
        #                     # For this example, let's just display the input values
        #     with col2:
        #         # with st.expander("2. Delete with csv file"):
        #                 # Upload CSV file
        #             uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        #             if uploaded_file:
        #                 df = pd.read_csv(uploaded_file)
        #                 st.write(df)
        #                 email_column = "Email"
        #                 email_addresses = df[email_column].tolist()

        #             # Delete button
        #                 if st.button("Delete", key="delete_button"):
        #                     count = 0
        #                     del_count=0
        #                     st.warning("under progress....kindly wait")
        #                     for email in email_addresses:
        #                         deleted = False  # To track if the record was deleted

        #                         # Iterate through collections to find the record
        #                         for collection, collection_archieves in [
        #                             (Account, Account_archieves),
        #                             (BankingFinance, BankingFinance_archieves),
        #                             (Finance, Finance_archieves),
        #                             (FoodSafety, FoodSafety_archieves),
        #                             (Healthcare, Healthcare_archieves),
        #                             (HumanResource, HumanResource_archieves),
        #                             (Insurance, Insurance_archieves),
        #                             (Pharmaceutical, Pharmaceutical_archieves)

        #                             # ... Other collections ...
        #                         ]:
        #                             query = {"Email": email}
        #                             results = collection.find(query)
        #                             doc_count = collection.count_documents(query)
        #                             if doc_count > 0:
        #                                 count=count+1
        #                                 # Move record to archives and delete from the collection
        #                                 for result in results:
        #                                     collection_archieves.insert_one(result)
        #                                 collection.delete_many(query)
        #                                 st.write(f"Record of {email} removed successfully from {collection.name}")
        #                                 deleted = True
        #                                 break  # Exit loop if record is found and deleted

        #                         if not deleted:
        #                             del_count=del_count+1

        #                     st.write("deleted records", del_count)
        #                     st.success("completed...............")
        #                     time.sleep(2)
        #                     st.experimental_rerun()  # Refresh the app


    elif navigation=="1. Update Client data":  
        updatepage.main()
    elif navigation=="2. Update Hardbounce":
        hardbounce.main()
    elif navigation=="4. Generate CSV file":
        generatecsv.main()



                    