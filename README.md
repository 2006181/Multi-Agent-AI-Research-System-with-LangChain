# 🔎 Multi-Agent AI Research System with LangChain

A multi-agent research assistant built with **LangChain**, **Groq**, and **Tavily**. Give it a topic, and a team of AI agents searches the web, reads the best source, writes a structured report, and then critiques its own work. It runs from the terminal or from a **Streamlit** web UI.

---

## ✨ Features

- **Search Agent** finds recent, reliable sources on your topic using the Tavily search API
- **Reader Agent** picks the most relevant URL and scrapes its content for deeper context
- **Writer Chain** drafts a structured report (Introduction, Key Findings, Conclusion, Sources)
- **Critic Chain** reviews the report, gives a score out of 10, and lists strengths and improvements
- **Streamlit UI** with live step-by-step progress, tabbed results, and a downloadable report
- **CLI mode** to run the whole pipeline directly in the terminal

---

## 🧠 How It Works

```
        ┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
Topic ─▶│   Search   │────▶│   Reader   │────▶│   Writer   │────▶│   Critic   │──▶ Report + Feedback
        │   Agent    │     │   Agent    │     │   Chain    │     │   Chain    │
        └────────────┘     └────────────┘     └────────────┘     └────────────┘
         web_search()        scrape_url()      LLM report        LLM review
          (Tavily)        (requests + BS4)
```

| Step | Component | What it does |
|------|-----------|--------------|
| 1 | Search Agent | Calls the `web_search` tool and returns titles, URLs, and snippets |
| 2 | Reader Agent | Chooses the most relevant URL and calls `scrape_url` to extract page text |
| 3 | Writer Chain | Combines search results and scraped content into a structured report |
| 4 | Critic Chain | Scores the report and gives feedback in a fixed format |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain / LangGraph** for agents and chains
- **Groq** (`openai/gpt-oss-120b`) as the LLM
- **Tavily** for web search
- **BeautifulSoup4 + Requests** for web scraping
- **Streamlit** for the web UI
- **python-dotenv** for environment variables

---

## 📁 Project Structure

```
Multi-Agent-AI-Research-System-with-LangChain/
├── agents.py          # LLM setup, search/reader agents, writer & critic chains
├── tools.py           # web_search (Tavily) and scrape_url tools
├── pipeline.py        # Runs the full pipeline in the terminal
├── app.py             # Streamlit web UI
├── check_models.py    # Lists the models available on your Groq account
├── requirements.txt   # Python dependencies
├── .env               # API keys (not committed)
└── .gitignore
```

---

## 🚀 Getting Started

## Deployment link 
streamlit - https://multi-agent-ai-research-system-with-langchain-ql8dqsdvwjlxnvmd.streamlit.app/

### 1. Clone the repository

```bash
git clone https://github.com/2006181/Multi-Agent-AI-Research-System-with-LangChain.git
cd Multi-Agent-AI-Research-System-with-LangChain
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

- Get a Groq key at [console.groq.com](https://console.groq.com)
- Get a Tavily key at [tavily.com](https://tavily.com)

> ⚠️ Never commit your `.env` file. Make sure it is listed in `.gitignore`.

---

## ▶️ Usage

### Option A: Streamlit UI (recommended)

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser, enter a research topic, and click **Run research**. You'll see each agent's progress live, and the results appear in four tabs:

- 📄 **Final Report** (downloadable as `.md`)
- 🧐 **Critic Feedback**
- 🔍 **Search Results**
- 📖 **Scraped Content**

### Option B: Terminal

```bash
python pipeline.py
```

Enter a topic when prompted. Every step's output is printed to the console.

### Check available Groq models

```bash
python check_models.py
```

---

## 📝 Example

**Topic:** `Impact of generative AI on railway logistics`

**Output:**
1. A list of recent sources with titles, URLs, and snippets
2. Detailed text scraped from the most relevant page
3. A structured report with Introduction, Key Findings, Conclusion, and Sources
4. A critic review in this format:

```
Score: 8/10

Strengths:
- ...

Areas to Improve:
- ...

One line verdict:
...
```

---

## 🔮 Future Improvements

- Scrape multiple URLs and merge the content
- Let the Writer revise the report using the Critic's feedback
- Export reports as PDF or DOCX
- Add a model selector and search depth controls in the UI
- Show clickable source citations in the report

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

---

## 👤 Author

Built by **Rahul** · [GitHub](https://github.com/2006181)
