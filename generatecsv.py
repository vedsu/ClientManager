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

Account_jobtitle = client['JobTitle_Account']

BankingFinance_jobtitle = client['JobTitle_BankingFinance']

Finance_jobtitle = client['JobTitle_Finance']

FoodSafety_jobtitle=client['JobTitle_FoodSafety']

Healthcare_jobtitle=client['JobTitle_Healthcare']

HumanResource_jobtitle = client['JobTitle_HumanResource']

Insurance_jobtitle = client['JobTitle_Insurance']

Pharmaceutical_jobtitle = client['JobTitle_Pharmaceutical']

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

Vedsu_Unsubscribe = db['Vedsu_Unsubscribe']

# Collections to exclude from the dropdown
collections_to_exclude = ["Account","Account_archieves", "Banking&Finance_archieves",  "Banking&Finance","Finance","Finance_archieves", "FoodSafety","FoodSafety_archieves",
                         "Healthcare", "Healthcare_archieves","HumanResource", "HumanResource_archieves","Insurance","Insurance_archieves",  "Pharmaceutical","Pharmaceutical_archieves", "Vedsu_Unsubscribe"]

existing_collections = db.list_collection_names()

filtered_collections = [col for col in existing_collections if col not in collections_to_exclude]

@st.cache_resource
def unique_email():
    distinct_email = []

    # Storing emails from hardbounce collections
    for hardbounce in filtered_collections:
        
        inusehardbounce = db[hardbounce]
        
        hardbounce_emails = inusehardbounce.distinct("Email")
        
        distinct_email.extend(hardbounce_emails)  # Extend the list with emails from this collection
    
    unsubscribe_emails = Vedsu_Unsubscribe.distinct("Email")
    
    distinct_email.extend(unsubscribe_emails)  # Extend the list with unsubscribe emails
    
    return distinct_email

    
def main():
    st.subheader("Generate CSV")

    options = ["Select", "Account", "Banking&Finance", "Finance", "FoodSafety", "Healthcare", "HumanResource", "Insurance", "Pharmaceutical"]

    selected_option = st.selectbox("Select an option", options)
    
    if selected_option == "Account":
        db_jobtitle = Account_jobtitle
        collection = Account
        collection_archieves = Account_archieves
        
    elif selected_option == "Banking&Finance":
        db_jobtitle = BankingFinance_jobtitle
        collection = BankingFinance
        collection_archieves = BankingFinance_archieves   
    
    elif selected_option == "Finance":
        db_jobtitle = Finance_jobtitle
        collection = Finance
        collection_archieves = Finance_archieves
    
    elif selected_option == "FoodSafety":
        db_jobtitle = FoodSafety_jobtitle
        collection = FoodSafety
        collection_archieves = FoodSafety_archieves
    
    elif selected_option == "Healthcare":
        db_jobtitle = Healthcare_jobtitle
        collection = Healthcare
        collection_archieves = Healthcare_archieves
        
    elif selected_option == "HumanResource":
        db_jobtitle = HumanResource_jobtitle
        collection = HumanResource
        collection_archieves = HumanResource_archieves
        
    elif selected_option == "Insurance":
        db_jobtitle = Insurance_jobtitle
        collection = Insurance
        collection_archieves = Insurance_archieves
    
    elif selected_option == "Pharmaceutical":
        db_jobtitle = Pharmaceutical_jobtitle
        collection = Pharmaceutical
        collection_archieves = Pharmaceutical_archieves
    
        
    st.success(f"You selected: {selected_option}")
    st.write("**************************************************************")
    query={}
    
    tog_value = tog.st_toggle_switch(label="Switch Search methods", 
                key="toggle_option", 
                default_value=False, 
                label_after = False, 
                inactive_color = '#D3D3D3', 
                active_color="#11567f", 
                track_color="#29B5E8"
                )
    user_job_titles =[]
    
    if tog_value==False:
        
        # Create a multitext_input widget
        search_terms = st.text_input(
        "Enter the search terms",
        placeholder="Enter job titles separated by commas",)
        
        # Split the user input into a list of job titles
        user_job_titles = [title.strip() for title in search_terms.split(',')]
    
    else:
        
        existing_collections = db_jobtitle.list_collection_names()
        
        jobtitle_collections = st.multiselect('Select Job Titles to search',existing_collections)
        
        st.write('You selected:', jobtitle_collections)
        
        
        
        for jobtitle_collection in jobtitle_collections:
        
            jobtitles = db_jobtitle[jobtitle_collection]
        
            user_job_titles.extend(jobtitles.distinct("JobTitle"))
        
        # Convert the list to a set to remove any remaining duplicates
        user_job_titles = list(set(user_job_titles))
        # st.write(user_job_titles)
    
    st.write("**************************************************************")
    
    if selected_option != "Select":
         # Allow user to input the start document index (which is a multiple of 100000)
        total_documents = collection.count_documents({})
        
        options = ["1 lac", "2 lac", "5 lac"]
        
        file_size = st.selectbox("Select file size", options, key="file_size_select")
        if file_size =="1 lac":
            batch=100000
        elif file_size =="2 lac":
            batch=200000
        elif file_size =='5 lac':
            batch=500000

        batch = int(batch / len(user_job_titles)) if len(user_job_titles)>0 else 0

        start_document = st.number_input(f"Start document index (multiple of {file_size}):", min_value=0, max_value=total_documents-1, value=0, key="input_value",step= batch)
        # Calculate the end document index

        offset = batch  # Set the desired offset value

        end_document = min(start_document + offset, total_documents - 1)
    
    
    generate_button = st.button("Click to generate the view")

    if generate_button:
        # Query the documents based on the user input
            st.warning("generating excel please wait...")

            # Construct a query condition for each user input
            archived_documents = []

            for user_job_title in user_job_titles:
                # Create a regex pattern for each input with flexibility (fuzzy search)
                regex_pattern = f".*{re.escape(user_job_title)}.*"

                # Define a query condition for the current input
                query = {
                    "$text": {
                        "$search": regex_pattern
                    },
                   
                }

                # Add the condition to the list
                query_results = collection.find(query).skip(start_document).limit(end_document - start_document + 1)
    
                # Get distinct emails
                distinct_emails = unique_email()

                # Process the query resultss
                
                for doc in query_results:
            
                    if doc["Email"] in distinct_emails:
            
                        # Delete from main collection and move to archieves
                        collection.delete_one({"_id": doc["_id"]})
            
                        existing_document = collection_archieves.find_one({ "Email":doc["Email"]})
            
                        if existing_document is None:
            
                            collection_archieves.insert_one(doc)
            
                    else:
                        
                        archived_documents.append(doc)
            
            st.success("excel file generated successfully")
            
            df = pd.DataFrame(archived_documents)
            
            # Select specific columns from archived_df to create df2 (projection)
            selected_columns = ["Date", "Email", "JobTitle", 'Status',"Department", "Industry"]
            
            df2 = df[selected_columns]
            
            st.dataframe(df2)
            
        
            csv_content= df2.to_csv(index=False)
            st.download_button(
                        label="Download CSV",
                        data=csv_content,
                        file_name="query_results.csv",
                        mime="text/csv")
       
        
        


