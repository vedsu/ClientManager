import streamlit as st
import pymongo
from dateutil import parser
import time
import pandas as pd
import datetime


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
# Collections to exclude from the dropdown
collections_to_exclude = ["Account","Account_archieves", "Banking&Finance_archieves",  "Banking&Finance","Finance","Finance_archieves", "FoodSafety","FoodSafety_archieves",
                         "Healthcare", "Healthcare_archieves","HumanResource", "HumanResource_archieves","Insurance","Insurance_archieves",  "Pharmaceutical","Pharmaceutical_archieves", "Vedsu_Unsubscribe"]

def create_collection(collection_name):
    db.create_collection(collection_name)
    st.sidebar.success(f"Collection '{collection_name}' created successfully.")
    time.sleep(1)

def main():
    st.sidebar.title("MongoDB Collection Creator")

    # Input field for collection name
    collection_name = st.sidebar.text_input("Enter collection name:")
    # Dropdown to select existing collections
    existing_collections = db.list_collection_names()
    filtered_collections = [col for col in existing_collections if col not in collections_to_exclude]
    st.write("------------------------------------------")
    selected_collections = st.selectbox("Select hardbounce platform:", filtered_collections)
    st.write("------------------------------------------")
    selected_collection = db[selected_collections]
    # Create collection button
    if st.sidebar.button("Create Collection", key="create_button"):
        if collection_name:
            create_collection(collection_name)
            
        else:
            st.sidebar.warning("Please enter a collection name.")
        st.experimental_rerun()

    with st.container():
            col1, col2 = st.columns(2)
            with col1:
                # with st.expander("1. Update Hardbounce"):
                        # Dropdown select box
                        email = st.text_input("Email:", value="")
            
                        # Update button
                        if st.button("Update") and email != "":
                            existing_document = selected_collection.find_one({"Email": email})
                            if existing_document:
                                st.warning(f"Email '{email}' already exists in the collection")
                            
                            else:
                                document = {"Email":email}
                                try: 
                                    selected_collection.insert_one(document)
                                  
                                    st.success(f"record inserted successfully")
                                except:
                                    st.error("record could not be inserted successfully")
                            
                            time.sleep(1)
            
        
                            st.experimental_rerun()
            
                        
            with col2:
                    # Upload CSV file
                    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
                    if uploaded_file:
                        df = pd.read_csv(uploaded_file)
                        st.write(df)
                        # Insert CSV data into the database
                        if st.button("Update" , key = "update_button"):
                            st.warning("uploading files to hardbounce, please wait")
                            # Create a set to store seen email addresses
                            seen_emails = set()
                            # Populate the set with existing email addresses from the collection
                            existing_emails = selected_collection.distinct("Email")
                            seen_emails.update(existing_emails)
                            st.write("Existing Emails : ", len(seen_emails))
                            
                            # Prepare a list to store data to insert
                            data_to_insert = []

                            # Iterate through DataFrame rows
                            
                            for index, row in df.iterrows():
                                email = row["Email"]
                                # If the email is already in the set, skip it
                                if email in seen_emails:
                                        
                                        # st.warning(f"Duplicate email '{email}' skipped.")
                                        continue

                                # If email is not in the set, add it to the seen_emails set
                                seen_emails.add(email)
                                # Append data to the list for bulk insertion
                                data_to_insert.append({
                                "Email": email
                                })
                            # Insert data into the desired collection using insert_many
                            try:
                                selected_collection.insert_many(data_to_insert)
                                st.success(f"Inserted {len(data_to_insert)} emails successfully.")
                            except Exception as e:
                                st.error(f"Error inserting data: {e}")

                            time.sleep(2)
                            st.experimental_rerun()  # Refresh the app
