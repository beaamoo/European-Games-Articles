import openai
import streamlit as st

def gptgeneration(event_df,ranking_df,info):
# Set up your OpenAI API credentials
    openai.api_key = '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'

    # Transform the df into text for the prompt
    # Load your DataFrame (replace with your actual DataFrame)

#Website to generate prompts: https://promptperfect.jina.ai/prompts
    input_text = f'''Compose a captivating blog article summarizing the medals that were awarded today (latest date) per sport and division, the changes in the overall ranking per country between yesterday and today, and the countries that climbed to the top of the podium and those that were displaced (mention those countries). Talk about the overall ranking exclusively in the end of the article (never mention the ranking before that in any of the other sections). In that section mention the countries that were in the podium the day before, and where they are now after the new medals, same with the ones that were able to get to the podium. also, say how many medals they have and how many medals each country won after today's events. 
                    Do not write the structure of the article with words such as 'introduction:' or 'conclusion:'. Use titles for each section (sport + division). For each, write a paragraph of less than 100 words, concisely recapping the athletes' outcomes and achievements, the ranking changes, and the podium with the countries with the highest number of medals attributed. 
                    Discuss the athletes' outcomes and achievements in a concise manner, highlighting their performances and the impact they made in their respective sports. Avoid using overly exaggerated language and focus on providing an engaging and informative recap of the events.{info}'''
    prompt = """Please regard the following data:\n {}. generate an article that will not have too many expressive words. do not say: incredible, amazing, thrilling,outstanding, remarkable skill, prowess. I do not want such expressiveness. be journalistic professional: {}""".format(event_df, ranking_df, input_text)
    st.markdown(prompt)
    # Call the ChatGPT API
    response = openai.Completion.create(
        engine='gpt-4-engine-name',
        prompt=prompt,
        max_tokens=1000,
        temperature=0.8,
        top_p=0.9,
    )

    # Retrieve the generated response
    generated_text = response.choices[0].text.strip()
    st.markdown(generated_text)

    return generated_text
