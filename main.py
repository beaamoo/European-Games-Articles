import pandas as pd
import streamlit as st
from df import get_the_data
from generation import gptgeneration
from doc import add_to_doc

st.title(f"You have selected Summary per country")

# Initialize session states
if "date_selection" not in st.session_state:
    st.session_state["date_selection"] = []

if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

# Button event to load data
if st.button('Get the data'):
    st.session_state["event_df"], st.session_state["ranking_df"] = get_the_data()
    st.session_state["data_loaded"] = True

# Display multiselect widget when the data is loaded
if st.session_state["data_loaded"]:
    unique_dates = st.session_state["event_df"]['Medal Date'].unique()
    st.session_state['date_selection'] = st.multiselect('Date:', unique_dates, default=st.session_state['date_selection'])

    previous_date = pd.to_datetime(st.session_state['date_selection']) - pd.DateOffset(days=1)
    filtered_df = st.session_state["event_df"][st.session_state["event_df"]['Medal Date'].isin(st.session_state['date_selection']) |
                                             st.session_state["event_df"]['Medal Date'].isin(previous_date)][['Discipline', 'Medal Type', 'Name', 'Medal Date']]

    # Make the table bigger
    styles = [
        dict(selector="table", props=[("font-size", "120%")]),
        dict(selector="th", props=[("font-size", "120%")]),
        dict(selector="td", props=[("font-size", "120%")])
    ]
    filtered_df_styled = filtered_df.style.set_table_styles(styles)

    # Show the styled table
    st.table(filtered_df_styled)
    print(filtered_df)

    # Additional text box
    add_info = st.text_area('Enter text: ')

    if st.button('Generate article'):
        text = gptgeneration(event_df=st.session_state["event_df"], ranking_df=st.session_state["ranking_df"], info=add_info)
        document_url = add_to_doc(text)
        st.markdown(f"Here is the link: {document_url}")