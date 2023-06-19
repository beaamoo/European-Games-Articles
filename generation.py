import openai
import streamlit as st

#tech lab: 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

def gptgeneration(event_df,ranking_df,info, schedule, date):
# Set up your OpenAI API credentials
    openai.api_key = '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'
    

    # Transform the df into text for the prompt
    # Load your DataFrame (replace with your actual DataFrame)

    #Website to generate prompts: https://promptperfect.jina.ai/prompts
    # Section for the dataframes
    event_df_section = f"Event Details:\n {event_df}"
    ranking_df_section = f"\nRanking Details:\n {ranking_df}"
    schedule_section = f"\nSchedule Details:\n {schedule}"

    # Input text
    input_text = f'''Compose a blog article for the European games 2023 in Krakow summarising today's medal awards across different sports and divisions, while bearing in mind today's date: {date}. 
                    Begin with a succinct overview of yesterday's events. Follow with the main body, divided into sections by sport, discussing athletes' performances, ranking shifts, and medal-winning nations. 
                    In the conclusion, discuss the overall medal standings. If there's a change in the podium, highlight the countries on yesterday's podium and their positions today, along with the new arrivals. If not, discuss the impacted countries. Limit to the top 5 countries in the rankings.
                    Don’t use labels like 'Introduction' or 'Conclusion'. Keep the introduction under 150 words, the main body within 600 words, and the conclusion under 150 words. Use a journalistic professional storytelling approach, do not use expressive words like incredible, amazing, thrilling, outstanding, remarkable skill, prowess. {info}'''

    metadata_keywords = f''' After the article, provide the metadata for the article (under 150 characters) and 5-10 unique keywords optimised for SEO'''

    # Prompt
    prompt = f'''{event_df_section} 
                {ranking_df_section} 
                {schedule_section} 
                {input_text}
                {metadata_keywords}'''

    st.title(f"Prompt")
    st.markdown(prompt)
    response = ""
    generated_text = ""


#GPT 3: text-davinci-003
#GPT 4: gpt-4-engine-name
    
    # Call the ChatGPT API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1000,
        temperature=0.8,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Retrieve the generated response
    generated_text = response.choices[0].text.strip()

    st.title(f"Article")
    st.markdown(generated_text)


    return generated_text


def lolgorithm(input):
# Set up your OpenAI API credentials
    openai.api_key = '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'

    # Prompt
    prompt = f'''Generate an article that will not have too many expressive words. do not say: incredible, amazing, thrilling,outstanding, remarkable skill, prowess. I do not want such expressiveness. You must be journalistic professional. This is the most important point. The output should be less than 100 words. {input}. '''

    # Call the ChatGPT API
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1000,
        temperature=0.8,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Retrieve the generated response
    generated_text = response.choices[0].text.strip()

    return generated_text


