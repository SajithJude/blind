import openai
import streamlit as st
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")



def generate_persona(feature_description):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate a persona based on the following feature: {feature_description}"},
        ]
    )
    return response['choices'][0]['message']['content']

def chat_with_persona(persona, message):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": f"You are {persona}."},
            {"role": "user", "content": message},
        ]
    )
    return response['choices'][0]['message']['content']

# Load existing personas
try:
    with open("db.json", "r") as f:
        personas = json.load(f)
except FileNotFoundError:
    personas = {}

# Generate a new persona
feature_description = st.text_input("Enter a feature description")
if st.button("Generate Persona"):
    persona = generate_persona(feature_description)
    st.write(persona)
    if 'personas' not in st.session_state:
        st.session_state.personas = {}
    st.session_state.personas[feature_description] = persona

    # Save the persona
    with open("db.json", "w") as f:
        json.dump(st.session_state.personas, f)

    st.success('Persona generated and saved successfully!')

# Chat with a selected persona
if 'personas' in st.session_state and st.session_state.personas:
    selected_persona_description = st.selectbox("Select a persona to chat with", options=list(st.session_state.personas.keys()))
    selected_persona = st.session_state.personas[selected_persona_description]
    message = st.text_input("Enter your message")
    if st.button("Send"):
        response = chat_with_persona(selected_persona, message)
        st.write(f"Persona's response: {response}")
