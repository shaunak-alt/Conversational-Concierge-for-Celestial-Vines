# 🍷 Conversational Concierge for Celestial Vines

This project is a smart, conversational AI agent for "Celestial Vines," a fictional Napa Valley vineyard. Built with LangChain and Streamlit, this agent acts as a virtual concierge, capable of answering a wide range of questions by intelligently using a set of tools.



## ✨ Features

This agent is equipped with three distinct tools to provide accurate and relevant information:

* **🍇 Vineyard Knowledge Base**: Answers specific questions about the vineyard's hours, wine selection, tour packages, and contact information using a Retrieval-Augmented Generation (RAG) system.
* **🌐 Real-time Web Search**: Performs live web searches using SerpAPI to answer general knowledge questions or provide information on current events.
* **☀️ Live Weather Updates**: Fetches the current weather for Napa Valley from the OpenWeatherMap API, perfect for visitors planning a trip.

---

## ⚙️ How It Works

The agent is built on the **ReAct (Reasoning and Acting)** framework. When a user asks a question, a powerful Language Model (LLM) from Hugging Face first **reasons** about which tool is best suited to answer it. Then, it **acts** by using the chosen tool, observes the output, and formulates a final, coherent response.

This multi-tool approach ensures the agent is not limited to a single source of information, making it flexible and powerful.

```
User Question
      |
      V
LLM (Mixtral) Reasons: "Which tool should I use?"
      |
      +-----------------+-----------------+-----------------+
      |                 |                 |                 |
      V                 V                 V                 V
"Is it about       "Is it about       "Is it a general   "I can answer
the vineyard?"     the weather?"     question?"        directly."
      |                 |                 |                 |
      V                 V                 V                 |
  Use RAG Tool     Use Weather Tool   Use Web Search        |
      |                 |                 |                 |
      +-----------------+-----------------+-----------------+
      |
      V
LLM Observes Tool Output & Generates Final Answer
      |
      V
Display to User
```

---

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

* Python 3.9+
* Git

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Create `requirements.txt`

Before installing, create a `requirements.txt` file by running this command in your activated virtual environment. This helps others install the exact versions of the packages you used.

```bash
pip freeze > requirements.txt
```

### 4. Install Dependencies

Now, install all the required packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5. Set Up API Keys

Create a file named `.env` in the root of your project folder. This file will store your secret API keys.

```env
# Get from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
HUGGINGFACEHUB_API_TOKEN="hf_..."

# Get from [https://serpapi.com/](https://serpapi.com/)
SERPAPI_API_KEY="..."

# Get from [https://openweathermap.org/api](https://openweathermap.org/api)
OPENWEATHERMAP_API_KEY="..."
```

---

## ▶️ How to Run

Once the setup is complete, you can run the Streamlit application with a single command:

```bash
streamlit run app.py
```

Your web browser will automatically open to the chat interface.

---

## 🛠️ Technology Stack

* **Frameworks**: LangChain, Streamlit
* **LLM**: `mistralai/Mixtral-8x7B-Instruct-v0.1` via Hugging Face
* **Tools & APIs**: SerpAPI, OpenWeatherMap
* **Embeddings & Vector Store**: Hugging Face Sentence Transformers, FAISS
* **Core Libraries**: `requests`, `python-dotenv`

---

## 💡 Future Improvements

* **Booking Integration**: Add a tool to simulate booking a wine tour.
* **Stateful Conversations**: Implement memory to recall previous parts of the conversation.
* **LangGraph Implementation**: Rebuild the agent logic using LangGraph for more complex, cyclical reasoning paths.
* **UI Enhancements**: Add features like example questions and chat history management.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
