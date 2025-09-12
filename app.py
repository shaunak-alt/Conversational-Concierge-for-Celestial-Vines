import streamlit as st
import os
import requests
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool, tool
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_huggingface import HuggingFaceEndpoint

# --- 1. Load API Keys ---
load_dotenv()

# Check for API keys
if not all(key in os.environ for key in ["HUGGINGFACEHUB_API_TOKEN", "SERPAPI_API_KEY", "OPENWEATHERMAP_API_KEY"]):
    st.error("Missing API keys in .env file. Please make sure HUGGINGFACEHUB_API_TOKEN, SERPAPI_API_KEY, and OPENWEATHERMAP_API_KEY are set.")
    st.stop()

# --- 2. Create the Tools ---

# Tool 1: Vineyard Information Retriever (RAG)
@st.cache_resource
def get_retriever_tool():
    # Create a dummy text file content in memory
    business_info_text = """
    Our Napa Valley vineyard, 'Celestial Vines', was founded in 1985.
    We are open from 10 AM to 5 PM, Tuesday to Sunday. We are closed on Mondays.
    We specialize in Cabernet Sauvignon and Chardonnay.
    Our most popular wine tasting package is the 'Sunset Tour', which costs $75 per person.
    The 'Sunset Tour' includes a guided tour of the vineyard and five wine samples.
    To book a tour or for any inquiries, visitors must call us at (707) 555-1234.
    Our address is 123 Vineyard Lane, Napa, CA 94558.
    """
    # Use RecursiveCharacterTextSplitter to split the text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    docs = text_splitter.create_documents([business_info_text])
    
    # Set up embeddings and FAISS vector store
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever()

    # Create the tool
    retriever_tool = create_retriever_tool(
        retriever,
        "vineyard_info_search",
        "Search for information about the Celestial Vines vineyard. Use this for questions about their hours, wine types, tours, and contact information."
    )
    return retriever_tool

# Tool 2: Web Search
@st.cache_resource
def get_web_search_tool():
    search = SerpAPIWrapper()
    return Tool(
        name="web_search",
        func=search.run,
        description="A tool for performing Google searches. Use this for answering questions about current events or general knowledge that is not about the vineyard."
    )

# Tool 3: Weather
@tool
def get_todays_weather(location: str) -> str:
    """Gets the current weather for a specific location. The location should always be 'Napa, US' for this business."""
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Always use Napa for this specific concierge
    fixed_location = "Napa,US"
    
    params = {"q": fixed_location, "appid": api_key, "units": "metric"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_desc = data['weather'][0]['description']
        temp = data['main']['temp']
        
        return f"The current weather in Napa Valley is {weather_desc} with a temperature of {temp}°C."
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather: {e}"
    except KeyError:
        return "Error: Could not parse weather data."

# --- 3. Create the Agent ---

@st.cache_resource
def create_agent():
    # Initialize the LLM
    llm = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        temperature=0.7,
        max_new_tokens=512
    )

    # Get all tools
    tools = [get_retriever_tool(), get_web_search_tool(), get_todays_weather]

    # Get the ReAct prompt template
    prompt = hub.pull("hwchase17/react")

    # Create the agent
    agent = create_react_agent(llm, tools, prompt)

    # Create the agent executor
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    return agent_executor

agent_executor = create_agent()

# --- 4. Build the Streamlit UI ---

st.title("🍷 Celestial Vines Concierge")
st.caption("Your AI assistant for our Napa Valley vineyard.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me about our wines, the weather, or anything else!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent_executor.invoke({"input": prompt})
            st.markdown(response['output'])
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response['output']})