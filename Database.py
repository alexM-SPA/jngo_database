import streamlit as st
import pandas as pd
import re
from Grantmaker import grantmakerView
from Recipient import recipientView

try:
    data19 = pd.read_csv("FoundationData19.21.csv"
                         , encoding= 'windows-1252')
except FileNotFoundError:
    st.error("Data file not found. Please check the file path.")
    st.stop()

cols = ["Recipient", "Foundation"]
def normalize(name):
    if pd.isna(name):
        return ""
    # lowercase, strip
    name = name.lower().strip()
    # remove punctuation (keep spaces & word chars)
    name = re.sub(r"[^\w\s]", "", name)
    # collapse multiple spaces
    name = re.sub(r"\s+", " ", name)
    return name

for col in cols:
    data19[f"{col}"] = data19[col].apply(normalize)


st.title("Grants Database 2019-2021")
st.text("Explore over 800 foundations and 44,000 recipient organizations.")

#Search bar and results
search_mode = st.selectbox("Search by:", ["Foundation", "Recipient"])
options = data19[search_mode].dropna().unique()
selected_name = st.selectbox(f"Select a {search_mode}:", sorted(options))
filtered_data = data19[data19[search_mode] == selected_name]



# Display institution data
if search_mode == "Recipient":
    recipientView(filtered_data, selected_name)

#Display donor data
elif search_mode == "Foundation":
        grantmakerView(filtered_data, selected_name)
