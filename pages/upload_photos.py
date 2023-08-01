import streamlit as st
import base64
import requests
import json
import os
from pathlib import Path
from llama_index import download_loader, GPTSimpleVectorIndex, SimpleDirectoryReader

st.set_option('deprecation.showfileUploaderEncoding', False)

# Title
st.title("Procastinated Preparation APP")

# OCR function
def callAPI(image):
    vision_url = 'https://vision.googleapis.com/v1/images:annotate?key='

    # Your Google Cloud Platform (GCP) API KEY. Generate one on cloud.google.com
    api_key = os.environ["GCP_KEY"] 
    # Load your image as a base64 encoded string

    # Generate a post request for GCP vision Annotation
    json_data= {
        'requests': [
            {
                'image':{
                    'content': image.decode('utf-8')
                },
                'features':[
                    {
                        'type':'TEXT_DETECTION',
                        'maxResults':5
                    }
                ]
            }
        ]
    }

    # Handle the API request
    responses = requests.post(vision_url+api_key, json=json_data)

    # Read the response in json format

    return responses.json()

# Text saver function
def save_text(text):
    os.makedirs('text', exist_ok=True)  # create directory if it doesn't exist
    file_name = f"{st.session_state.photo_name.split('.')[0]}.txt"
    file_path = os.path.join("text", file_name)
    with open(file_path, 'w') as f:
        f.write(text)
        # st.write('Text saved to file:', file_path)

# Photo taker
uploaded_files = st.file_uploader("Upload photos of your book", type=["jpg", "png"], accept_multiple_files=True)
st.session_state['img'] = uploaded_files

if len(st.session_state['img']) > 0:
    if "generate" not in st.session_state:
        st.success("Clear photos to upload new ones or Generate to continue")
        i = 1
        for x in st.session_state['img']:
            st.write(str(i)+" "+str(x.name), key=i)
            i = i+1
    generate_button = st.button("Generate")
    if generate_button or "generate" in st.session_state:
        st.session_state['generate'] = True
        if generate_button:
            st.experimental_rerun()
            # Get the photo name to save the text file with the same name
            
        st.session_state['info'] = []
        # OCR and save text file
        j = 1
        for x in st.session_state['img']:
            st.session_state.photo_name = f"photo_{st.session_state.get('photo_counter', 0)}.jpg"
            st.session_state.photo_counter = st.session_state.get("photo_counter", 0) + 1
            encoded_image = base64.b64encode(x.read())
            result = callAPI(encoded_image)
            # try:
            info = result['responses'][0]['textAnnotations'][0]['description']

        
            st.write(str(j)+" "+str(x.name), key=j)
            st.caption("Text Recognized")
            st.write(info+"\n\n")
            save_text(info)

            # Create index from text directory
            text_dir = os.path.join(os.getcwd(), "text")
            # st.write(text_dir)
            # if text_dir.exists():
            index_path = text_dir
            # if not index_path.exists():
            documents = SimpleDirectoryReader(str(text_dir)).load_data()
            intax = GPTSimpleVectorIndex.from_documents(documents)
            res= intax.query("Generate 5 Questions with answers from this documents")
            
            st.caption("Questions generated:\n")
            st.info(str(res)+"\n\n")
            st.markdown("""---""")
            for file in os.listdir(text_dir):
                file_path = os.path.join(text_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    # st.info("cache cleared")
                except Exception as e:
                    print(e)
            j = j +1
        print("Text directory cleared")