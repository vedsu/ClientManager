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

Vedsu_HardBounce = db["Vedsu_HardBounce"]
Vedsu_Unsubscribe = db['Vedsu_Unsubscribe']



def main():
        st.subheader("Update Hardbounce/Unsubscribe")
        options = ["Unsubscribe", "Hardbounce"]
        st.write("-------------------------------------------------------------")
        selected_option = st.selectbox("Select an option", options)
        st.write("-------------------------------------------------------------")
        if selected_option == "Unsubscribe":
            unsubscribe()
        else:
            hardbounce()
             
def hardbounce():
    with st.container():
            col1, col2 = st.columns(2)
            with col1:
                # with st.expander("1. Update Hardbounce"):
                        # Dropdown select box
                        email = st.text_input("Email:", value="")
                        bounce_reason = st.text_input("Reason:", value="")
                        bounce_description = st.text_input("Description:", value="")
            
                        # Update button
                        if st.button("Update") and email != "":
                            existing_document = Vedsu_HardBounce.find_one({"Email": email})
                            if existing_document:
                                st.warning(f"Email '{email}' already exists in the collection")
                            
                            else:
                                document = {"Email":email, "Bounce_Reason":bounce_reason, "Bounce_Description": bounce_description }
                                try: 
                                    Vedsu_HardBounce.insert_one(document)
                                  
                                    st.success(f"record inserted successfully")
                                except:
                                    st.error("record could not be inserted successfully")
                            
                            time.sleep(1)
            
        
                            st.experimental_rerun()
            
                            

                            # Perform the deletion or processing here
                            # For this example, let's just display the input values
            with col2:
                # with st.expander("2. Update with csv file"):
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
                            existing_emails = Vedsu_HardBounce.distinct("Email")
                            seen_emails.update(existing_emails)
                            st.write(len(seen_emails))
                            
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
                                 # Check if "Bounce_Reason" and "Bounce_Description" columns exist in the row
                                if "Bounce_Reason" in row and "Bounce_Description" in row:
                                    bounce_reason = row["Bounce_Reason"]
                                    bounce_description = row["Bounce_Description"]
                                else:
                                    bounce_reason = ""
                                    bounce_description = ""

                                # Append data to the list for bulk insertion
                                data_to_insert.append({
                                "Email": email,
                                "Bounce_Reason": bounce_reason,
                                "Bounce_Description": bounce_description
                                })
                            # Insert data into the desired collection using insert_many
                            # try:
                            st.success(f"Inserted {len(data_to_insert)} emails successfully.")
                            Vedsu_HardBounce.insert_many(data_to_insert)
                            # except:
                            st.error("Error inserting data, try again")
                        
                            time.sleep(1)
                            st.experimental_rerun()  # Refresh the app
def unsubscribe():
    with st.container():
            col1, col2 = st.columns(2)
            with col1:
                # with st.expander("1. Update Unsubscribe"):
                        # Dropdown select box
                        emailid = st.text_input("Email:", value="")
                        reason = st.text_input("Reason:", value="")
                        unsubscribebrand = st.text_input("UnsubscribeBrand:", value="")
                        createDate = st.date_input("Date:")
                        # Convert createDate to a datetime object
                        create_datetime = datetime.datetime.combine(createDate, datetime.time.min)
            
                        # Update button
                        if st.button("Update") and emailid != "":
                            existing_document = Vedsu_Unsubscribe.find_one({"Email": emailid})
                            if existing_document:
                                st.warning(f"Email '{emailid}' already exists in the collection")
                            
                            else:
                                documents = {"Email":emailid, "Reason": reason, "UnsubscribeBrand":unsubscribebrand, "CreateDate":create_datetime}
                                try: 
                                    Vedsu_Unsubscribe.insert_one(documents)
                                  
                                    st.success(f"record inserted successfully")
                                except:
                                    st.error("record could not be inserted successfully")
                            
                            time.sleep(1)
        
                            st.experimental_rerun()
                            

                            # Perform the deletion or processing here
                            # For this example, let's just display the input values
            with col2:
                # with st.expander("2. Update with csv file"):
                    try:    # Upload CSV file
                        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
                    except:
                        st.write("file fromat not supported")
                    if uploaded_file:
                        df = pd.read_csv(uploaded_file)
                        st.write(df)
                        if st.button("Update" , key="update_unsubscribe"):# Insert CSV data into the database
                            st.warning("uploading files to Unsubscribe, please wait")
                            # Create a set to store seen email addresses
                            seen_emails = set()
                            # Populate the set with existing email addresses from the collection
                            existing_emails = Vedsu_HardBounce.distinct("Email")
                            seen_emails.update(existing_emails)
                            
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
                                 # Check if "Bounce_Reason" and "Bounce_Description" columns exist in the row
                                if "Bounce_Reason" in row and "Bounce_Description" in row:
                                    bounce_reason = row["Bounce_Reason"]
                                    bounce_description = row["Bounce_Description"]
                                else:
                                    bounce_reason = ""
                                    bounce_description = ""

                                # Append data to the list for bulk insertion
                                data_to_insert.append({
                                "Email": email,
                                "Bounce_Reason": bounce_reason,
                                "Bounce_Description": bounce_description
                                })
                            # Insert data into the desired collection using insert_many
                            try:
                                Vedsu_HardBounce.insert_many(data_to_insert)
                                st.success(f"Inserted {len(data_to_insert)} emails successfully.")
                            except:
                                st.error("Error inserting data, try again")
                        
                            time.sleep(1)
                            st.experimental_rerun()  # Refresh the app
                            