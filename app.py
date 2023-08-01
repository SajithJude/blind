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

st.subheader("Capture Photos")
st.info("In this section, you can capture single or multiple pages of a book using your camera. Our smart assistant will analyze the captured images and generate a set of questions with answers related to the content of the book pages. This is a great way to quickly test your understanding of the material you're reading, or to explore new topics.")

st.subheader("Upload Books")
st.info("In the Upload Books section, you can upload any PDF book to chat with our intelligent Book Assistant. Simply upload a PDF file, and our assistant will index the content, allowing you to ask questions about the book. This feature enables you to dive deeper into your reading, gain valuable insights, and enhance your learning experience.")


st.subheader("Upload Photos")
st.info("In this section, you can upload photos of single or multiple pages of a book using your camera. Our smart assistant will analyze the captured images and generate a set of questions with answers related to the content of the book pages. This is a great way to quickly test your understanding of the material you're reading, or to explore new topics.")



st.write("Get started by selecting one of the options from the navigation menu, and enjoy your interactive learning journey with our Procastinated Preparation APP!")
