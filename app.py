import streamlit as st
import psycopg2
from psycopg2 import sql
import pandas as pd

### postgres 
PGEND_POINT='database-1.ch8kew8yio67.ap-south-1.rds.amazonaws.com'
PGDATABASE_NAME='postgres_db'
PGUSER_NAME='postgres'
PGPASSWORD='akash213$'

## Title of application
st.title("LLM Search Places")

# Create a text input field
user_input = st.text_input("Enter places you have visited:")
        
        
def connect():
    conn_string = "host="+PGEND_POINT+" port="+ "5432" +" dbname="+ PGDATABASE_NAME +" user=" + PGUSER_NAME \
        +" password=" +PGPASSWORD
    
    conn = psycopg2.connect(conn_string)
    print("Connected")
    
    #create cursor object
    cursor = conn.cursor
    return conn, cursor

        
# Function to connect to PostgreSQL and insert data
def save_to_db(user_input):
    try:
        conn, cur = connect()

        # insert some data
        places_visited_insert = sql.SQL("""
        INSERT INTO places_visited (place) VALUES (%s);""")
        ##places_visited_insert = sql.SQL("""INSERT INTO places_visited (place) VALUES ('2005, i visited london');""")
        print("User input -----",user_input)
        cur = conn.cursor()
        cur.execute(places_visited_insert,[user_input])
        cur.close()
        conn.commit()

        return True
    except Exception as e:
        return str(e)
    
# Function to query data from the 'places_visited' table
def query_places():
    try:
        # Connect to AWS PostgreSQL
        conn, cur = connect()
        cur = conn.cursor()

        # Execute the query
        query_places = sql.SQL("SELECT * FROM places_visited;")
        cur.execute(query_places)

        # Fetch the results
        rows = cur.fetchall()
        print("Rowa-----",rows)

        # Get column names
        colnames = [desc[0] for desc in cur.description]
        print("colnames====",colnames)

        # Close the connection
        cur.close()
        conn.close()

        # Return data as a DataFrame
        return pd.DataFrame(rows, columns=colnames)
    except Exception as e:
        return str(e)
    


## Create a submit button to user input to AWS POSTGRES DB 
if st.button("Submit"):
    if user_input:
        result = save_to_db(user_input)
        if result is True:
            st.success("Text saved to database successfully!")
        else:
            st.error(f"Failed to save text: {result}")
    else:
        st.write("Please enter some text before submitting.")
    
## Section to query and display data to Streamlit from AWS Postgres DB
st.header("Places Visited")
if st.button("Show all places visited"):
    data = query_places()
    print("Data -----",data)
    if isinstance(data, pd.DataFrame):
        st.write(data)
    else:
        st.error(f"Failed to fetch data: {data}")
