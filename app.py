import streamlit as st
import pandas as pd

# Load data using Spark SQL
data = spark.sql("SELECT * FROM customer_orders2").toPandas()

def chatbot(query):
    query = query.lower().strip()
    
    if "total price" in query and "for" in query:
        customer_name = query.split("for")[-1].strip()
        sql_query = f"""
            SELECT SUM(TotalPrice) AS Total_Price
            FROM customer_orders2
            WHERE LOWER(CustomerName) LIKE '%{customer_name}%'
        """
        result = spark.sql(sql_query).collect()[0]["Total_Price"]
        if result:
            return f"The total price for {customer_name.title()} is {result}."
        else:
            return f"No data found for customer '{customer_name.title()}'."
    
    elif "orders from" in query:
        country = query.split("from")[-1].strip().upper()
        sql_query = f"SELECT * FROM customer_orders2 WHERE UPPER(Country) = '{country}'"
        result = spark.sql(sql_query).toPandas()
        if not result.empty:
            return result.to_string(index=False)
        else:
            return f"No orders found for '{country}'."

    else:
        return "Query not recognized. Please try again."

# Streamlit Web App
st.title("Interactive Chatbot - Customer Orders")
st.write("Ask the chatbot about the dataset!")

query = st.text_input("Enter your query:")
if st.button("Submit"):
    response = chatbot(query)
    st.write(response)

