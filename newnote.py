from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
import os
import streamlit as st

genai.configure(api_key=os.getenv("googleapikey"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
  generation_config=generation_config,
  safety_settings=safety_settings)
st.set_page_config(page_title="Note.AI")

st.title("Note.AI")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

grade=st.text_input("Enter Grade/Year: ",key="input")
curr=st.text_input("Enter Curriculum: ",key="input2")
subject=st.text_input("Enter Subject: ",key="input3")
topic=st.text_input("Enter Topic: ",key="input4")
exam=st.text_input("Enter Exam: ",key="input5")
extra=st.text_input("Enter Extra Details/Notes: ",key="input6")
submit=st.button("Generate Notes...")
prompt_parts = [
  "I am a student looking to revise for my exams. my current grade is:",grade,", my current curriculum is ",curr,", the subject i am studying for is",subject,", the topic i am studying is ",topic,", and the exam i am studying for is ",exam,". Here are some extra details : ",extra,". I need in-depth revision notes, and eg if it is maths or science if there are any formulas etc add them and give me examples and how to use them etc, if it is english etc add any analysis required with the quotes and themes and everything etc, if it is history etc add any key words, dates, people, etc etc. Please create in depth revision notes for this based on the above data that can help a student achieve good marks in the exam. it should be minimum 500 words.",
]
if submit and grade and curr and subject and topic and exam:
  st.write("Please wait a few seconds while Note.AI creates your notes...")
  response = model.generate_content(prompt_parts)
  st.header("Notes: ")
  st.write(response.text)
  st.session_state['chat_history'].append(("Note.AI: ", response.text))
  st.header("\nWould you like to alter something specific? Write a short sentence and put it in the 'extra details' input box, and press generate!")
st.header("Chat History:")
    
for role, text in st.session_state['chat_history']:
  st.write(f"{role}: {text}")
    
