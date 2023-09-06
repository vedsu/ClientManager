import streamlit as st
import pymongo
from dateutil import parser
import time
import pandas as pd
import datetime
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
db= client['ClientDatabase']
Vedsu_Unsubscribe = db['Vedsu_Unsubscribe']


def main():
        st.subheader("Update Unsubscribe")
        unsubscribe()
       

def unsubscribe():
    with st.container():
            
            tog_value = tog.st_toggle_switch(label="Switch upload methods", 
                key="toggle_option", 
                default_value=False, 
                label_after = False, 
                inactive_color = '#D3D3D3', 
                active_color="#11567f", 
                track_color="#29B5E8"
                )

            
            if tog_value==False:

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
            else:
                
                    try:    
                        # Upload CSV file
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
                            existing_emails = Vedsu_Unsubscribe.distinct("Email")
                        
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

                                # Append data to the list for bulk insertion
                                data_to_insert.append({
                                "Email": email
                                })
                        
                            # Insert data into the desired collection using insert_many
                            try:
                        
                                Vedsu_Unsubscribe.insert_many(data_to_insert)
                        
                                st.success(f"Inserted {len(data_to_insert)} emails successfully.")
                            except:
                        
                                st.error("Error inserting data, try again")
                        
                            time.sleep(1)
                        
                            st.experimental_rerun()  # Refresh the app
                        
