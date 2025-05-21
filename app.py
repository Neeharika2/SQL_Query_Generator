from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import requests

load_dotenv() 

API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")
API_URL = "https://openrouter.ai/api/v1/chat/completions"


def get_response(question,prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        sql = response.json()["choices"][0]["message"]["content"].strip()
        return sql
    else:
        st.error("API Error: " + response.text)
        return None



def connect_db(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

prompt="""
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Retrieving SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

if submit:
    response = get_response(question, prompt)
    if response:
        if response.strip().lower().startswith("select"):
            results = connect_db(response, "student.db")
            st.subheader("The Response is:")
            for row in results:
                st.write(row)
        else:
            st.error("Generated query is not a SELECT statement.")