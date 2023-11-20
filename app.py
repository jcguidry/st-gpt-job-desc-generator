import streamlit as st
import openai
import time
import os
from src.openai_st import stream
from src.rag import Retriever, appendMessageHistoryContext

openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_job_description_prompt(company, title, location, requirements, tone, salary_range):
    
    system_instructions = "You are a job description generator. You are given a company name, job title, location, and key requirements. You must generate a job description for the role."

    # prompt = (
    #     f"Generate a job description for the following role:\n"
    #     f"Company Name: {company}\n"
    #     f"Job Title: {title}\n"
    #     f"Location: {location}\n"
    # )

    # job_title = 'Senior Provider Data Management Analyst'
    # company = 'Molina Healthcare'
    # location = 'Long Beach, CA'
    # requirements = 'Bachelors degree in related field'
    # tone = 'professional'
    # salary_range = '$73,102 - $142,549 per year'

    prompt = f"""
        Draft a job description for the role listed in the Job Title field below. Using the requirements and gerneral tone also specified below, delimited in '''.
        Include a short 'About Us' section about the company seeking candidates for this positon.
        Company: '''{company}'''
        Job Title: '''{title}'''
        Location: '''{location}'''
        Key Requirements: '''{requirements}'''
        Tone: '''{tone}'''
        Salary Range: '''{salary_range}'''
    """

    messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": prompt},
        ]
    
    return messages


# # For testing
# generate_job_description('infosys', 'data science consultant', 'Dallas, TX', 'demand forecasting')


# Create the app
st.set_page_config(page_title='Job Description Generator', page_icon=':robot_face:')
st.title("Job Description Generator")

# Input fields
model_type = st.selectbox("Model Type", options=["GPT-3.5 (faster)", "GPT-4 (smarter)"])
model_id_lookup = {"GPT-3.5 (faster)": "gpt-3.5-turbo", "GPT-4 (smarter)": "gpt-4-0314"}
model_id = model_id_lookup[model_type]

use_rag = st.toggle("Use RAG", value=False)

# Variables for prompt
company_name = st.text_input("Company Name", value="Molina Healthcare")
job_title = st.text_input("Job Title", value="Senior Provider Data Management Analyst")
location = st.text_input("Location", value="Long Beach, CA")
key_requirements = st.text_area("Key Requirements", value="Bachelors degree in related field, Experience with Master Data Management, Relational Database knowledge, Python, SQL")
tone = st.text_input("Tone", value="Professional")

# salary_range = st.slider("Salary Range", min_value=0, max_value=200000, value=(50000, 100000), step=1000, format="$%d")
salary_range_min = st.number_input("Minimum Salary", 73102)
salary_range_max = st.number_input("Maximum Salary", 142549)
salary_range = f'${salary_range_min} - ${salary_range_max} per year'

# On "Generate" button click
if st.button("Generate", type="primary"):
    if company_name and job_title and location and key_requirements:
        
        # Call the function to generate a job description
        messages = generate_job_description_prompt(company_name, job_title, location, key_requirements, tone, salary_range)

        messages_primary_prompt = messages[1]['content']
        
        if use_rag:
            # perform similarity search on the job description prompt
            document_context = Retriever().retrieve(messages_primary_prompt, k=1) 
            st.header("Document Context")
            st.write(document_context)
            messages = appendMessageHistoryContext(messages, document_context)

        st.divider()
        st.header("Job Description")
        
        # Create a placeholder for the output
        box = st.empty()

        # Call openai in streaming fashion
        stream(model=model_id, prompt=messages, box=box)
        current_text = stream.s

        st.download_button('Download as text file', current_text , file_name=f'Job Description - {job_title}.txt', mime='text/plain')

    else:
        st.warning("Please fill in all the fields.")