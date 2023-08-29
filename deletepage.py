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
                        if st.button("Update" , key = "update_button"):# Insert CSV data into the database
                            st.warning("uploading files to hardbounce, please wait")
                            for index, row in df.iterrows():
                                existing_document = Vedsu_HardBounce.find_one({"Email": row["Email"]})
                                if existing_document is None:
                                    data_to_insert = {
                            "Email": row["Email"],
                            "Bounce_Reason": row["Bounce_Reason"],
                            "Bounce_Description": row["Bounce_Description"]}
                                # Insert data into the desired collection
                                    try:
                                        Vedsu_HardBounce.insert_one(data_to_insert)
                                    except:
                                        st.error("please check the csv file again")

                            st.success("Uploaded successfully")

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
                            for index, row in df.iterrows():
                                existing_document = Vedsu_Unsubscribe.find_one({"Email": row["Email"]})
                                if existing_document is None:
                                    data_to_insert = {
                            "Email": row["Email"],
                            "UnsubscribeBrand": row["UnsubscribeBrand"],
                            "Reason": row["Reason"],
                            "CreateDate": row["CreateDate"]}
                                # Insert data into the desired collection
                                    try:
                                        Vedsu_Unsubscribe.insert_one(data_to_insert)
                                    except:
                                        st.error("please check the csv file again")

                            st.success("Uploaded successfully")

                            time.sleep(1)
                            st.experimental_rerun()  # Refresh the app
