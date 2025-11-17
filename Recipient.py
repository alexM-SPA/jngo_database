import streamlit as st
import plotly.express as px
from Grantmaker import convert_df

def recipientView(filtered_data, selected_name, award_column="AWARD"):
    #
    if award_column in filtered_data.columns:
        top_awards = (
            filtered_data.groupby('Foundation', as_index=False)[award_column]
            .sum()
            .sort_values(by=award_column, ascending=False)
            .head(5)
        )
        st.subheader("Philanthropic Activity 2019-2021")
        fig = px.bar(top_awards, x='Foundation', y=award_column, title=f"Top Donors to {selected_name}")
        st.plotly_chart(fig)

    #Donation Table by Recipient
    st.write("Major Donors:")
    all_grants = (
        filtered_data.groupby('Foundation', as_index=False)[award_column]
        .sum()
        .sort_values(by=award_column, ascending=False)
        .rename(columns={award_column: "Total Donations ($)"}))

    all_grants_display = all_grants.copy()
    all_grants_display["Total Donations ($)"] = all_grants_display["Total Donations ($)"].apply(lambda x: f"${x:,.2f}")
    st.write(all_grants_display)

    # Category Banner
    categories = filtered_data['Category'].dropna().unique()
    category_list = ", ".join(categories)
    st.subheader(f"{selected_name} is active in the {category_list} sector.")

    st.text("A profile on this organization may be available here:")
    if st.button("Reports"):
        st.switch_page("Reports.py")

    #Download data
    st.text("Download donation data for this organization here:")

    csv = convert_df(all_grants)
    st.download_button(
    label = "CSV",
    data = csv,
    file_name = f"{selected_name}_data.csv",
    mime = 'text/csv',
    key = 'download-org-csv'
    )
