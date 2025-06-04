import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd
import logging
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def color_threshold(val, threshold=50):
    """Color values above threshold in green, below in red"""
    if pd.isna(val):
        return ''
    color = 'background-color: #ffcdd2' if val < threshold else 'background-color: #c8e6c9'  # Light red/green
    return color

# Load environment variables
load_dotenv()

# Get API URL from environment variable or use a default
BASE_API_URL = os.getenv("PROCUREMENT_API_URL", "http://localhost:8080")
API_URL = f"{BASE_API_URL}/api/v1/search/procurement_query"
logger.info(f"Using API URL: {API_URL}")

st.set_page_config(
    page_title="Procurement Assistant",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ Procurement Assistant")
st.markdown("""
This app helps you query the procurement database using natural language.
Simply type your question about products, suppliers, or procurement data below.
""")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask a question about procurement data...")
if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show a spinner while waiting for the API response
    with st.spinner("Thinking..."):
        try:
            # Make API request with the correct payload format
            logger.info(f"Sending request to {API_URL}")
            payload = {
                "natural_query": prompt,
                "limit": 10
            }
            logger.info(f"Request payload: {json.dumps(payload)}")
            
            response = requests.post(
                API_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content: {response.text[:200]}...")  # Log first 200 chars of response
            
            response.raise_for_status()
            
            # Get the response
            result = response.json()
            
            # Display the response
            with st.chat_message("assistant"):
                if isinstance(result, dict) and "entries" in result:
                    # Extract relevant fields from entries
                    products = []
                    for entry in result["entries"]:
                        fields = entry["fields"]
                        product = {
                            "Name": fields["name"],
                            "Category": fields["category"],
                            "Brand": fields["brand"],
                            "Department": fields["department"],
                            "Cost": fields["cost"],
                            "Retail Price": fields["retail_price"],
                            "Profit Margin": fields["profit_margin_percent"],
                            "Total Orders": fields["total_orders"],
                            "Return Rate": fields["return_rate_percent"],
                            "Supplier Score": fields["supplier_reliability_score"],
                            "Total Revenue": fields["total_revenue"],
                            "Items Sold": fields["total_items_sold"]
                        }
                        products.append(product)
                    
                    # Create DataFrame
                    df = pd.DataFrame(products)
                    
                    # Style the DataFrame
                    st.dataframe(
                        df.style
                        .format({
                            "Cost": "${:.2f}",
                            "Retail Price": "${:.2f}",
                            "Total Revenue": "${:.2f}",
                            "Profit Margin": "{:.1f}%",
                            "Return Rate": "{:.1f}%",
                            "Supplier Score": "{:.1f}"
                        })
                        .applymap(color_threshold, subset=["Profit Margin", "Supplier Score"]),
                        use_container_width=True
                    )
                    
                    # Add summary statistics
                    st.markdown("### Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average Cost", f"${df['Cost'].mean():.2f}")
                    with col2:
                        st.metric("Average Profit Margin", f"{df['Profit Margin'].mean():.1f}%")
                    with col3:
                        st.metric("Total Products", len(df))
                else:
                    st.markdown(str(result))
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": str(result)
            })
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            with st.chat_message("assistant"):
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Make sure the API URL is correct and the service is running.")
                st.code(f"API URL: {API_URL}\nPayload: {json.dumps(payload, indent=2)}", language="text")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {str(e)}"
            })

# Add a sidebar with information
with st.sidebar:
    st.header("About")
    st.markdown("""
    This app connects to a procurement API running on Google Cloud Run.
    
    You can ask questions like:
    - "What are the top 5 products by price?"
    - "Show me all products from supplier X"
    - "What are the most expensive items in category Y?"
    """)
    
    st.header("API Status")
    try:
        health_check = requests.get(f"{BASE_API_URL}/health")
        if health_check.status_code == 200:
            st.success("API is healthy and running")
        else:
            st.error("API is not responding correctly")
    except:
        st.error("Cannot connect to API")
    
    st.header("Settings")
    st.text_input("API URL", value=BASE_API_URL, key="api_url", 
                 help="The base URL of your Cloud Run API endpoint") 