import streamlit as st
from llama_index import GPTSimpleVectorIndex, Document, SimpleDirectoryReader, QuestionAnswerPrompt
import os
import openai 
from streamlit_chat import message as st_message

import os
import streamlit as st
from tempfile import NamedTemporaryFile
import PyPDF2
# from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
import openai
from pathlib import Path
from llama_index import download_loader



st.set_page_config(page_title="Upload material and chat", page_icon=None)

os.environ['OPENAI_API_KEY']  = "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"

openai.api_key = os.getenv("OPENAI_API_KEY")



if "history" not in st.session_state:
    st.session_state.history = []

def process_pdf(uploaded_file):
    PDFReader = download_loader("PDFReader")
    loader = PDFReader()
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        documents = loader.load_data(file=Path(temp_file.name))
    return documents

def delete_file(DATA_DIR, file_name):
    pdf_path = os.path.join(DATA_DIR, file_name)
    json_path = os.path.join(DATA_DIR, os.path.splitext(file_name)[0] + ".json")
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        st.success(f"File {file_name} deleted successfully!")
    else:
        st.error(f"File {file_name} not found!")
    if os.path.exists(json_path):
        os.remove(json_path)

def save_uploaded_file(uploaded_file):
    with open(os.path.join(DATA_DIR, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

def new_chat():
    st.session_state.history = []

DATA_DIR = "data"
if not os.path.exists("data"):
    os.mkdir("data")

with st.expander("Upload/Delete books"):
    st.subheader("PDF books Management Portal")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)
        st.success("It would take a while to index the books, please wait..!")
    
        pdf_filename = uploaded_file.name
        
        documents = process_pdf(uploaded_file)
        index = GPTSimpleVectorIndex.from_documents(documents)
        index.save_to_disk(os.path.join(DATA_DIR, os.path.splitext(pdf_filename)[0] + ".json"))
        st.success("Index created successfully!")
    
    files = os.listdir(DATA_DIR)
    files = [f for f in files if not f.endswith(".json")]

    colms = st.columns((4, 1))

    fields = ["Name", 'Delete']
    for col, field_name in zip(colms, fields):
        col.subheader(field_name)

    i=1
    for Name in files:
        i+=1
        col1, col2 = st.columns((4 , 1))
        col1.caption(Name)
        delete_status = True if Name.endswith(".pdf") else False
        button_type = "Delete" if delete_status else "Gone"
        button_phold = col2.empty()
        do_action = button_phold.button(button_type, key=i, on_click=delete_file, args=(DATA_DIR, Name))

index_filenames = [f for f in os.listdir(DATA_DIR) if f.endswith(".json")]


if index_filenames:
    # If there are index files available, create a dropdown to select the index file to load
    index_file = st.selectbox("Select a book to chat with:", index_filenames)
    index_path = os.path.join(DATA_DIR, index_file)
    index = GPTSimpleVectorIndex.load_from_disk(index_path)
else:
    # If there are no index files available, prompt the user to upload a PDF file
    st.warning("No index files found. Please upload a PDF file to create an index.")
    

def generate_answer():
    user_message = st.session_state.input_text
    query_str = str(user_message)
    message_bot = index.query(query_str, response_mode="compact", mode="embedding")
    st.session_state.history.append({"message": user_message, "is_user": True})
    st.session_state.history.append({"message": str(message_bot), "is_user": False})
    st.session_state.input_text = ""
    # st.session_state.history = [{"message": user_message, "is_user": True},
    #                             {"message": str(message_bot), "is_user": False}]

if st.sidebar.button("New Chat"):
    new_chat()





input_text = st.text_input("Ask PDF_BOT Virtual Assitant a question", key="input_text", on_change=generate_answer)

if st.session_state.history:
    chat = st.session_state.history[-1]
    st_message(**chat)

for chat in st.session_state.history:

    if chat["is_user"]:

        st.sidebar.caption("Question: " + chat["message"])
    else:
        with st.sidebar.expander("Bot Answer", expanded=False):
            st.write(chat["message"], language=None)

def st_message(message, is_user):
    if is_user:
        st.write("You: " + message)
    else:
        st.write("PDF_BOT: " + message)