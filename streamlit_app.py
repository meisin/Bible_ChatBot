import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader

openai.api_key = st.secrets.openai_key

# Streamlit Page Configuration
st.set_page_config(
    page_title="Your Bible ChatBot",
    page_icon="image/bible.png",
    layout="wide",
    menu_items={
        "Get help": "https://github.com/meisin/Bible_ChatBot",
        "Report a bug": "https://github.com/meisin/Bible_ChatBot",
        "About": """
            ## Your Bible ChatBot
            
            **GitHub**: https://github.com/meisin/Bible_ChatBot
            
            This chatbot is built as a project to demonstrate the ability of Large Language Models in answering questions based on specific sources of information (in this case the Bible). It does quite well in Comprehension-like questions BUT may not work so well on Theological questions. We strongly suggest that you direct these questions to a pastor or any church leader.
        """
    }
)

st.header('Your Bible ChatBot')
st.title('Ask me anything in the Bible!')

# Load and display sidebar image with glowing effect
with st.sidebar:
        st.image('./image/bible.png')

st.sidebar.markdown("This chatbot is built as a project to demonstrate the ability of Large Language Models in answering questions based on specific sources of information (in this case the Bible). It does quite well in Comprehension-like questions BUT may not work so well on Theological questions. We strongly suggest that you direct these questions to a pastor or any church leader. ")
st.sidebar.markdown("---")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about the contents in the Bible and I will try my best to answer."}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the contents of the Bible. This should take 1-2 minutes."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.3, system_prompt="You are an expert on the bible and your job is to answer bible-related questions. Assume that all questions are related to the books in the Bible. Keep your answers based on facts found in the collection of documents– do not hallucinate features. Respond \"Sorry, this is not found in the Bible.\" if not sure about the answer"))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history


# tutorial : https://discuss.streamlit.io/t/build-a-chatbot-with-custom-data-sources-powered-by-llamaindex/49973
