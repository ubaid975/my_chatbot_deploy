import streamlit as st
from langchain_groq import ChatGroq
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import WikipediaQueryRun
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api = os.getenv("groq")

# Initialize the LangChain components
chat_groq = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=groq_api,
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
api_wrapper = WikipediaAPIWrapper(top_k_results=1)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

tools = [wiki]
agent = initialize_agent(tools, llm=chat_groq, memory=memory, agent="conversational-react-description")

# Streamlit app
st.title("Chat with RoboX")
st.write("Ask me anything!")

user_input = st.text_input("Type your message here:")

if st.button("Send"):
    if user_input:
        if "your name" in user_input.lower():
            st.write("My name is RoboX. I am a large language model developed by Ubaid.")
        else:
            try:
                response = agent.run(user_input)
                st.write(f"RoboX: {response}")
            except Exception as e:
                st.write("There was an issue processing your request.")




