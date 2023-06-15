import pandas as pd
import requests
from time import sleep
from fake_useragent import UserAgent
import json
import csv
import io

def get_the_data():
    ua = UserAgent()

    headers = {
        'User-Agent': ua.random,
    }

    url = "https://wrs-egt-cdn.mth.mev.atos.net/data/GLO_Medallists~comp=EG2023~lang=ENG.json"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        # Now you can process data as a normal Python dictionary
        print(data) # Just an example, replace this line with your data processing code
        sleep(2)
    else:
        print("Failed to access page")

    # Parse the JSON data
    parsed_data = data

    # Extract the desired information from the JSON data
    extracted_data = []
    for medallist in parsed_data['medallist']:
        discipline = medallist['discipline'].get('description')
        medal_type = medallist.get('medal_type')
        medal_date = medallist.get('medal_date')

        participant = medallist.get('participant', {})
        name = participant.get('name')
        birth_date = participant.get('birthDate')
        gender_code = participant.get('personGender', {}).get('code')
        organization = participant.get('organisation', {}).get('description')

        event_description = medallist.get('event', {}).get('longDescription')

        # Append the extracted data to a list
        extracted_data.append(
            [discipline, medal_type, medal_date, name, birth_date, gender_code, organization, event_description])

    # Save the extracted data to a CSV file
    with open('extracted_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Discipline', 'Medal Type', 'Medal Date', 'Name', 'Birth Date', 'Gender Code', 'Organization',
                         'Event Description'])
        writer.writerows(extracted_data)

    extracted_data = pd.read_csv('extracted_data.csv')

# Convert 'Medal Type' values to meaningful string representations
    extracted_data['Medal Type'] = extracted_data['Medal Type'].map({1: 'Gold', 2: 'Silver', 3: 'Bronze'})

# Pivot the DataFrame to get counts for each medal type by Organization
    pivot_df = pd.pivot_table(extracted_data, index='Organization', columns='Medal Type', aggfunc='size', fill_value=0)

    # Rename columns to match the requested output
    pivot_df.columns.name = None

    # If your pandas version is lower than 1.3.0, pivot_table does not sort the columns as expected.
    # In that case, reorder the columns manually as: Gold, Silver, Bronze.
    pivot_df = pivot_df[['Gold', 'Silver', 'Bronze']]

    # Add a 'Total' column
    pivot_df['Total'] = pivot_df.sum(axis=1)

    # Reset index to make 'Organization' a normal column again
    pivot_df.reset_index(inplace=True)

    # Sort DataFrame by 'Total' in descending order and reset the index again to get the 'Rank'
    pivot_df.sort_values('Total', ascending=False, inplace=True)
    pivot_df.reset_index(drop=True, inplace=True)

    # Add 'Rank' column based on the index (+1 because Python uses zero-based indexing)
    pivot_df.index += 1
    pivot_df.reset_index(inplace=True)
    pivot_df.rename(columns={'index': 'Rank'}, inplace=True)

    return extracted_data, pivot_df

