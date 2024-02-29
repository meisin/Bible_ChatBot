import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader

openai.api_key = st.secrets.openai_key
st.header("Chat with the Holy Bible")

st.title('🎈 App Name')

st.write('Hello world!')
