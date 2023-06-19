import pandas as pd
import streamlit as st
from df import get_the_data
from generation import gptgeneration
from doc import add_to_doc
from streamlit_option_menu import option_menu
from PIL import Image
import streamlit.components.v1 as components



# Load image
img = Image.open('Logos.png')

# Convert image to data URL
import base64
import io

def get_image_data_url(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return "data:image/png;base64," + img_str

# Build custom HTML
html_string = f"""
    <div style="display: flex; justify-content: center;">
        <img src="{get_image_data_url(img)}" style="height: 100px; margin-top: 0px;">
    </div>
"""

# Display custom HTML
st.components.v1.html(html_string, height=120)


st.title(f"Generate you summary per country article")
# Display the Option menu
selected = option_menu(
    menu_title= None,
    options= ['Summary per country', 'LOLgorithm', 'Reserve Articles', 'About the project', 'Creators'],
    icons=['graph-up', 'clipboard-data'],
    menu_icon= "cast",
    default_index= 0,
    orientation='horizontal',)

if selected == 'Summary per country':
    st.write('')
    # Initialize session states
if "date_selection" not in st.session_state:
    st.session_state["date_selection"] = []

if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

# Button event to load data
if st.button('Get the data'):
    st.session_state["event_df"], st.session_state["ranking_df"] = get_the_data()
    st.session_state["Medals"] = pd.read_csv("Medals.csv", sep=';')  # Save the DataFrame to the session state
    st.session_state["data_loaded"] = True

# Display multiselect widget when the data is loaded
if st.session_state["data_loaded"]:
    unique_dates = st.session_state["event_df"]['Medal Date'].unique()
    st.session_state['date_selection'] = st.multiselect('Date:', unique_dates,
                                                        default=st.session_state['date_selection'])

    # Convert date_selection to datetime and subtract 1 day for 'previous_date'
    previous_date = (pd.to_datetime(st.session_state['date_selection']) - pd.DateOffset(days=1)).strftime('%Y-%m-%d')

    # Filter 'event_df' to include rows where 'Medal Date' matches the selected date or the previous date
    filtered_df = st.session_state["event_df"][
        (st.session_state["event_df"]['Medal Date'].isin(st.session_state['date_selection'])) |
        (st.session_state["event_df"]['Medal Date'].isin(previous_date))][['Discipline', 'Medal Type', 'Name', 'Medal Date']]

    # Assuming that 'Medals' df and 'event_df' are in the same session_state
    medals_df = st.session_state["Medals"]

    # Converting date_selection to date_time and adding 1 day
    next_dates = (pd.to_datetime(st.session_state['date_selection']) + pd.DateOffset(days=1)).strftime('%Y-%m-%d')

    # Create a list of columns to keep in the new Medals dataframe
    columns_to_keep = ['Sport'] + [date for date in next_dates if date in medals_df.columns]

    # Create the new filtered Medals dataframe
    filtered_medals_df = medals_df[columns_to_keep]

    # Drop rows with any missing values
    schedule = filtered_medals_df.dropna()

    # Convert numeric columns to integers
    for col in schedule.columns:
        if schedule[col].dtype == 'float64':
            schedule[col] = schedule[col].astype(int)

    # Make the table bigger
    styles = [
        dict(selector="table", props=[("font-size", "120%")]),
        dict(selector="th", props=[("font-size", "120%")]),
        dict(selector="td", props=[("font-size", "120%")])
    ]
    filtered_df_styled = filtered_df.style.set_table_styles(styles)

    # Show the styled table
    st.table(filtered_df_styled)
    filtered_df = filtered_df.sort_values(by='Medal Date')
    print(filtered_df)

    # Additional text box
    add_info = st.text_area('Enter text: ')

    if st.button('Generate article'):
        text = gptgeneration(event_df=st.session_state["event_df"], ranking_df=st.session_state["ranking_df"], info=add_info, schedule = schedule, date = st.session_state['date_selection'])
        document_url = add_to_doc(text)
        st.markdown(f"Here is the link: {document_url}")
    
elif selected == 'LOLgorithm':
    pass
elif selected == 'Reserve Articles':
    pass
elif selected == 'About the project':
    pass
elif selected == 'Creators':
    pass
