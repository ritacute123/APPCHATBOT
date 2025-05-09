import streamlit as st
import pandas as pd
import os

# Path to the CSV file (Updated Path)
DATA_PATH = "C:\\Users\\ktabi\\Downloads\\customer_orders.csv"

# Load data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv(DATA_PATH)
        return data
    except FileNotFoundError:
        st.error(f"File not found: {DATA_PATH}")
        return pd.DataFrame()

data = load_data()

# Chatbot function
def chatbot(query):
    query = query.lower().strip()

    # Check if data is loaded
    if data.empty:
        return "Data not found or failed to load."

    # Total price for a specific customer
    if "total price" in query and "for" in query:
        customer_name = query.split("for")[-1].strip().title()
        result = data[data["CustomerName"].str.contains(customer_name, case=False)]
        if not result.empty:
            total_price = result["TotalPrice"].sum()
            return f"The total price for {customer_name} is {total_price}."
        else:
            return f"No data found for customer '{customer_name}'."

    # Quantity of a specific product
    elif "how many" in query:
        product_list = data["Product"].str.lower().unique()
        for product in product_list:
            if product in query:
                quantity = data[data["Product"].str.lower() == product]["Quantity"].sum()
                return f"The total quantity sold for {product.title()} is {quantity} units."
        return "Product not found."

    # Orders from a specific country
    elif "orders from" in query:
        country = query.split("from")[-1].strip().title()
        result = data[data["Country"].str.contains(country, case=False)]
        if not result.empty:
            return result.to_string(index=False)
        else:
            return f"No orders found for '{country}'."

    # Most expensive product sold
    elif "most expensive product" in query:
        most_expensive = data.loc[data["PricePerUnit"].idxmax()]
        return f"The most expensive product sold was {most_expensive['Product']} at {most_expensive['PricePerUnit']} per unit."

    # Highest order value
    elif "highest order value" in query:
        highest_order = data.loc[data["TotalPrice"].idxmax()]
        return f"The highest order value was {highest_order['TotalPrice']} by {highest_order['CustomerName']}."

    # Total revenue
    elif "total revenue" in query:
        total_revenue = data["TotalPrice"].sum()
        return f"The total revenue generated is {total_revenue}."

    # Unique products sold
    elif "unique products" in query:
        unique_products = data["Product"].nunique()
        return f"The number of unique products sold is {unique_products}."

    # Default response
    else:
        return "Query not recognized. Please try again."

# Streamlit Web App
st.title("Interactive Chatbot - Customer Orders")
st.write("Ask the chatbot about the dataset!")

query = st.text_input("Enter your query:")
if st.button("Submit"):
    response = chatbot(query)
    st.write(response)
