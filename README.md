<div align="center">
  <a href="https://github.com/AyushGU12/MULTI-AGENT-SUPPORT">
    <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=250&section=header&text=MULTI-AGENT-SUPPORT&fontSize=60&animation=fadeIn&fontAlignY=35&desc=Autonomous%20AI%20agents%20that%20research%20the%20web%20and%20draft%20comprehensive%20articles&descAlignY=55&descSize=20" alt="Hero Banner" width="100%" />
  </a>

  <h3><a href="https://github.com/AyushGU12/MULTI-AGENT-SUPPORT">Live Demo</a> • <a href="#-architecture">Architecture</a> • <a href="#-installation--setup">Installation</a> • <a href="#-api-documentation">API Docs</a></h3>

  <p align="center">
    <a href="https://github.com/AyushGU12/MULTI-AGENT-SUPPORT/stargazers"><img src="https://img.shields.io/github/stars/AyushGU12/MULTI-AGENT-SUPPORT?style=for-the-badge&color=ffd700&logo=github&logoColor=white" alt="Stars" /></a>
    <a href="https://github.com/AyushGU12/MULTI-AGENT-SUPPORT/network/members"><img src="https://img.shields.io/github/forks/AyushGU12/MULTI-AGENT-SUPPORT?style=for-the-badge&color=00a8ff&logo=github&logoColor=white" alt="Forks" /></a>
    <a href="https://github.com/AyushGU12/MULTI-AGENT-SUPPORT/issues"><img src="https://img.shields.io/github/issues/AyushGU12/MULTI-AGENT-SUPPORT?style=for-the-badge&color=e84118&logo=github&logoColor=white" alt="Issues" /></a>
    <a href="https://github.com/AyushGU12/MULTI-AGENT-SUPPORT/blob/main/LICENSE"><img src="https://img.shields.io/github/license/AyushGU12/MULTI-AGENT-SUPPORT?style=for-the-badge&color=4cd137&logo=mit&logoColor=white" alt="License" /></a>
  </p>
  
  <a href="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=20&duration=4000&pause=1000&color=6366F1&center=true&vCenter=true&width=600&lines=Multi-Agent+AI+Collaboration;Powered+by+LangGraph+%26+AutoGen;Gemini+2.5+Flash+Orchestration;Real-Time+Event+Streaming;Next-Level+3D+React+Frontend">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=500&size=20&duration=4000&pause=1000&color=6366F1&center=true&vCenter=true&width=600&lines=Multi-Agent+AI+Collaboration;Powered+by+LangGraph+%26+AutoGen;Gemini+2.5+Flash+Orchestration;Real-Time+Event+Streaming;Next-Level+3D+React+Frontend" alt="Typing SVG" />
  </a>
</div>

<br />

---

## 🚀 Professional Overview

**MULTI-AGENT-SUPPORT** is a robust, production-ready AI workflow engine that leverages **LangGraph** and **AutoGen** to orchestrate highly autonomous AI agents. Powered by **Google Gemini 2.5 Flash**, it automates the entire research and synthesis lifecycle. A `Researcher` agent autonomously scours the live web using DuckDuckGo, while a `Writer` agent synthesizes the findings into beautifully structured markdown. 

This is paired with an industry-leading, **Visually Stunning React 3D Interface** utilizing Framer Motion, React Three Fiber, and TSParticles to stream real-time Server-Sent Events (SSE) from the FastAPI backend. 

### ✨ Why this project stands out:
- **True Autonomy**: Bypasses strict LLM chat formats by assigning concrete roles to distinct agents that collaborate and self-correct.
- **Enterprise Streaming**: Utilizes real-time SSE over FastAPI to provide instantaneous UX feedback while long-running LLM inferences process.
- **Aesthetic Dominance**: Goes far beyond standard templates, implementing physics-based animations, glassmorphism, and live WebGL 3D rendering in the browser.

---

## 🧠 System Architecture

MULTI-AGENT-SUPPORT operates on a decoupled Microservices architecture. 

```mermaid
graph TB
    subgraph Client [Visually Stunning React Frontend]
        UI[App.jsx] --> |1. User Inputs Topic| SSE[EventSource Client]
        SSE --> |3. Stream Events| UI
        UI --> 3D[AICore3D Rendering]
        UI --> MD[Markdown Parser]
    end

    subgraph Backend [FastAPI Server]
        API[api.py] --> |2. Invoke Workflow| LG[LangGraph Engine]
        LG --> |Event: Researcher Start| API
        LG --> |Event: Writer Start| API
    end
    
    subgraph Agents [Agentic Logic]
        LG --> R[Researcher Agent]
        R --> |Search Query| DDG[DuckDuckGo Search API]
        DDG --> |Live Results| R
        R --> |Passes Notes| W[Writer Agent]
        W --> |Inference| GEM[Gemini 2.5 Flash API]
        GEM --> |Draft Output| W
        W --> |Event: Complete| API
    end
    
    Client --> Backend
    Backend --> Agents
    
    style UI fill:#6366f1,color:#fff
    style API fill:#10b981,color:#fff
    style LG fill:#8b5cf6,color:#fff
```

<details>
<summary><b>Click to View High-Level Data Flow Sequence</b></summary>

```mermaid
sequenceDiagram
    participant User
    participant ReactUI
    participant FastAPI
    participant LangGraph
    participant Researcher
    participant Writer
    
    User->>ReactUI: Enters Topic & Clicks Generate
    ReactUI->>FastAPI: POST /api/research { topic }
    FastAPI->>LangGraph: app.stream(inputs)
    LangGraph->>Researcher: Start Node
    Researcher->>FastAPI: yield status "Researcher started..."
    FastAPI-->>ReactUI: SSE data
    Researcher->>Writer: Return research notes to state
    Writer->>FastAPI: yield status "Writer started..."
    FastAPI-->>ReactUI: SSE data
    Writer->>LangGraph: Return final draft
    LangGraph->>FastAPI: yield COMPLETE + Markdown data
    FastAPI-->>ReactUI: SSE data + Stream Ends
    ReactUI->>User: Display rendered article
```
</details>

---

## 🛠️ Tech Stack & Badges

<div align="center">
  
  **Frontend**<br>
  <img src="https://skillicons.dev/icons?i=react,vite,css,html,js" alt="Frontend Stack" />

  **Backend**<br>
  <img src="https://skillicons.dev/icons?i=python,fastapi" alt="Backend Stack" />
  
  **AI & APIs**<br>
  <img src="https://img.shields.io/badge/LangGraph-000?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph" />
  <img src="https://img.shields.io/badge/AutoGen-005571?style=for-the-badge&logo=microsoft&logoColor=white" alt="AutoGen" />
  <img src="https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini" />
  
</div>

---

## 📂 Project Structure

```text
📦 MULTI-AGENT-SUPPORT
 ┣ 📂 frontend               # Vite React Application
 ┃ ┣ 📂 src
 ┃ ┃ ┣ 📂 components
 ┃ ┃ ┃ ┣ 📜 AICore3D.jsx       # React Three Fiber 3D Element
 ┃ ┃ ┃ ┗ 📜 ParticleNetwork.jsx # TSParticles interactive bg
 ┃ ┃ ┣ 📜 App.jsx              # Main UI & SSE consumer
 ┃ ┃ ┣ 📜 index.css            # Glassmorphism & Animations
 ┃ ┃ ┗ 📜 main.jsx             # React entry
 ┃ ┣ 📜 package.json
 ┃ ┗ 📜 vite.config.js
 ┣ 📜 api.py                 # FastAPI backend entrypoint
 ┣ 📜 langgraph_app.py       # LangGraph Orchestration logic
 ┣ 📜 autogen_app.py         # Alternative AutoGen implementation
 ┣ 📜 requirements.txt       # Python dependencies
 ┗ 📜 README.md              # You are here
```

---

## ✨ Features

- ✅ **Autonomous Multi-Agent Collaboration**: Two distinct AI personas operating simultaneously.
- ✅ **Real-time Server-Sent Events (SSE)**: Watch the agents think and pass data live without polling.
- ✅ **React Three Fiber Integration**: 3D objects embedded in the DOM responding to application state.
- ✅ **Dynamic Fault Tolerance**: Fallback protocols implemented if rate-limits block live web searching.
- 🔄 **Dockerization**: Containerization process for seamless Kubernetes deployment.
- 📌 **OAuth2 Authentication**: Planned integration with Clerk for user management.

---

## ⚙️ Installation & Setup

### Prerequisites
- Node.js (v18+)
- Python (3.11+)
- Google Gemini API Key

### Local Setup

**1. Clone the repository**
```bash
git clone https://github.com/AyushGU12/MULTI-AGENT-SUPPORT.git
cd MULTI-AGENT-SUPPORT
```

**2. Setup Backend (FastAPI)**
```bash
# Create and activate virtual environment
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn langchain langchain-google-genai duckduckgo-search langgraph pyautogen

# Run the server
export GEMINI_API_KEY="your-api-key"
python api.py
```

**3. Setup Frontend (React)**
```bash
# In a new terminal, navigate to frontend
cd frontend

# Install high-performance UI libraries
npm install

# Start the Vite development server
npm run dev
```

Visit `http://localhost:5173` to interact with the agents!

---

## 📡 API Documentation

### `POST /api/research`

Triggers the LangGraph agent pipeline and opens a streaming connection.

**Request Body:**
```json
{
  "topic": "The future of quantum computing"
}
```

**Response: `text/event-stream`**
```json
data: {"agent": "researcher", "status": "Researcher finished its task.", "data": ""}

data: {"agent": "writer", "status": "Writer finished its task.", "data": "# The Future of Quantum...\n\nQuantum..."}

data: {"agent": "system", "status": "COMPLETE"}
```

---

## 🛡️ Security & Performance Considerations

- **API Security**: The architecture hides the Gemini API key securely on the backend server. The frontend never possesses or transmits sensitive tokens.
- **CORS Handling**: `api.py` utilizes robust CORS middleware to allow modular deployment of the frontend.
- **Scalability**: By utilizing FastAPI's `asyncio` architecture alongside LangGraph's `.stream()`, the backend is inherently non-blocking and can handle hundreds of concurrent agent executions efficiently.
- **Error Boundaries**: DuckDuckGo search rate limits are actively caught and handled using robust `try/except` logic, instructing the `Writer` agent to fallback onto the model's internal paramaterized weights.

---



## 🤝 Contributing

We welcome contributions from the community! Please read our [Contributing Guide](CONTRIBUTING.md) to understand our branching strategy and pull request process.

### Commit Convention
| Emoji | Meaning |
| :---: | :--- |
| ✨ | Introducing new features |
| 🐛 | Fixing a bug |
| 📝 | Writing docs |
| 🎨 | Improving structure / format of the code |

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" width="100%" />
  
  <b>Built with ❤️ by <a href="https://github.com/AyushGU12">AyushGU12</a></b>
  
  If you find this project useful, please consider giving it a ⭐!
</div>
