import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


def grantmakerView(filtered_data, selected_name, award_column="AWARD"):
    #
    if award_column in filtered_data.columns:
        top_awards = (
            filtered_data.groupby('Recipient', as_index=False)[award_column]
            .sum()
            .sort_values(by=award_column, ascending=False)
            .head(5)
        )
        st.subheader("Philanthropic Activity 2019-2021")
        fig = px.bar(top_awards, x='Recipient', y=award_column, title=f"Top Recipients from {selected_name}")
        st.plotly_chart(fig)

    #Donation Table by Recipient & Category
    st.write("All Institutions Receiving Donations:")
    all_orgs = (
        filtered_data.groupby(['Recipient', 'Category'], as_index=False)[award_column]
        .sum()
        .sort_values(by=award_column, ascending=False)
        .rename(columns={award_column: "Total Donations ($)"})
    )
    all_orgs_display = all_orgs.copy()
    all_orgs_display["Total Donations ($)"] = all_orgs_display["Total Donations ($)"].apply(lambda x: f"${x:,.2f}")
    all_orgs_display = all_orgs_display.reset_index(drop=True)
    st.write(all_orgs_display)

    # Category Table
    st.write("Category Activity:")
    categories = (
        all_orgs.groupby('Category', as_index=False)["Total Donations ($)"]
        .sum()
        .sort_values(by='Total Donations ($)', ascending=False)
    )
    categories_display = categories.copy()
    categories_display["Total Donations ($)"] = categories_display["Total Donations ($)"].apply(lambda x: f"${x:,.2f}")
    categories_display = categories_display.reset_index(drop=True)
    st.write(categories_display)

    # Download CSV of Merged Data
    mergeData = pd.merge(all_orgs_display, categories_display, how="outer")
    csv = convert_df(mergeData)

    #Pie charts for Jewish/Not-Jewish, Location
    st.subheader("Donation Destinations")

    figJ = px.pie(filtered_data, values='AWARD', names='Jewish/Non-Jewish', title="Recipient Goal", )
    st.plotly_chart(figJ, theme=None)

    figL = px.pie(filtered_data, values='AWARD', names='Location', title="Recipient Location", )
    st.plotly_chart(figL, theme=None)

    st.download_button(
    label = "Download Donations (CSV)",
    data = csv,
    file_name = f"{selected_name}_data.csv",
    mime = 'text/csv',
    key = 'download-org-csv'
    )
