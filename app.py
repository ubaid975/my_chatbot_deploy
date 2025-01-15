from langchain_groq import ChatGroq
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import WikipediaQueryRun
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import streamlit as st
import os
from gradio import ChatInterface
import gradio as gr
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor
from langchain.chains import LLMMathChain
import time
import gradio as gr
import streamlit as st
from threading import Thread
import time




import os
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import WikipediaQueryRun
load_dotenv()
groq_api=os.getenv("groq")


chat_groq = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=groq_api,
    # other params...
)
os.environ["SERPER_API_KEY"]=os.getenv("serper_api_key")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
api_w=WikipediaAPIWrapper(top_k_results=1)
wiki=WikipediaQueryRun(api_wrapper=api_w)


tools = load_tools(["google-serper"], llm=chat_groq)
math_chain = LLMMathChain(llm=chat_groq)
tool=[wiki,tools,math_chain]

agent = initialize_agent(
    tools, llm=chat_groq,memory=memory,agent="conversational-react-description",
)



def chat(text,history):
    try:
        gfg=text 
        if 'your name' in gfg or 'tumhara name' in gfg or 'tumhara naam' in gfg or 'tumhara nam' in gfg or "tumahara naam" in gfg or 'you name' in gfg:
            return 'My name is RoboX i am a large language model Developed by Ubaid'
        else:
 
            reponese=agent.run(gfg)
            print(f"Human:{gfg}\nAi:{reponese}")
            return reponese
    except Exception as e:
        return 'your internet issue'

app=ChatInterface(fn=chat,theme=gr.themes.Ocean())
def run_gradio():
    app.launch(show_error=True, share=False)
run_gradio()
st.components.v1.iframe(src="http://127.0.0.1:7868", width=800, height=600)



