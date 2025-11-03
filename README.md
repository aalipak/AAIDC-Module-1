<p align="center">
  <img src="https://img.icons8.com/external-flatart-icons-outline-flatarticons/64/000000/artificial-intelligence.png" width="80" alt="AI Logo"/>
</p>

<h1 align="center">🤖 AI Interview Simulator and Feedback System</h1>

<p align="center">
  <b>An intelligent RAG-based (Retrieval-Augmented Generation) system for simulating technical interviews with detailed, adaptive feedback.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python_3.8+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Framework-RAG-brightgreen" />
  <img src="https://img.shields.io/badge/Database-ChromaDB-orange" />
  <img src="https://img.shields.io/badge/License-MIT-blue" />
</p>

---

## 📚 Overview

**AI Interview Simulator** is an intelligent **Retrieval-Augmented Generation (RAG)** system designed to simulate **technical interviews** and provide **constructive, personalized feedback**. It uses a structured knowledge base of software development concepts to generate realistic, adaptive interview sessions.

---

## 🎯 Key Features

### 🗣️ Interactive Interview Simulation
- Conducts natural, context-aware technical interviews
- Maintains conversation memory for follow-up questions
- Adapts difficulty based on responses

### 📚 Comprehensive Knowledge Base
- Software Development Life Cycle (SDLC)
- Object-Oriented Programming (OOP)
- Backend & Frontend Development
- Database Systems
- Software Architecture
- MERN Stack Integration

### 💡 Smart Feedback System
- Evaluates technical accuracy
- Suggests areas for improvement
- Recommends additional learning resources
- Tracks user progress throughout the session

---

## ⚙️ Technical Implementation

### 🧩 Architecture

The system follows a **RAG (Retrieval-Augmented Generation)** architecture composed of the following layers:

<details>
<summary><b>Document Processing</b></summary>

- Loads technical interview content from structured text files
- Chunks content into manageable pieces
- Generates embeddings for semantic retrieval
</details>

<details>
<summary><b>Vector Database</b></summary>

- Stores embeddings using **ChromaDB**
- Performs semantic search for relevant context
- Maintains conversation history for contextual continuity
</details>

<details>
<summary><b>LLM Integration</b></summary>

- Supports multiple LLM providers (**OpenAI**, **Groq**, **Google**)
- Uses custom prompts for dynamic question generation
- Preserves conversation context for natural interaction
</details>

---

## 🧠 Knowledge Base Structure

```
data/
├── backend.txt                        # Backend development concepts
├── database.txt                       # Database systems and design
├── frontend.txt                       # Frontend development topics
├── mern_integration.txt               # MERN stack implementation
├── oop.txt                            # Object-oriented programming
├── software_architecture.txt          # System design principles
└── software_development_lifecycle.txt # SDLC processes
```

---

## 🚀 Getting Started

### 🧰 Prerequisites
- Python 3.8 or higher
- One of the following API keys:
  - OpenAI API key
  - Groq API key
  - Google AI API key

### 🛠️ Installation

```bash
# Clone the repository
git clone [your-repo-url]
cd interview-simulator

# Install dependencies
pip install -r requirements.txt
```

### ⚙️ Configure Environment Variables

Create a `.env` file in the root directory and add your API key:

```bash
OPENAI_API_KEY=your_key_here
# or
GROQ_API_KEY=your_key_here
# or
GOOGLE_API_KEY=your_key_here
```

---

## 🔄 Conversation Flow

<details>
<summary><b>🧠 Interview Initiation</b></summary>

- Loads relevant domain knowledge
- Establishes initial conversation context
- Sets interview difficulty level
</details>

<details>
<summary><b>💬 Question Generation</b></summary>

- Dynamically selects questions from the knowledge base
- Adjusts difficulty based on user responses
- Generates contextual follow-up questions
</details>

<details>
<summary><b>🧩 Response Analysis</b></summary>

- Evaluates technical accuracy
- Assesses conceptual understanding
- Measures knowledge depth
</details>

<details>
<summary><b>📊 Feedback Generation</b></summary>

- Provides detailed feedback and improvement suggestions
- Recommends resources for continued learning
- Tracks progress over time
</details>

---

## 📈 Future Enhancements

### 🧠 Extended Knowledge Base
- More technical domains
- Updated best practices
- Industry-specific interview content

### 💬 Enhanced Interaction
- Mock coding exercises
- System design challenges
- Real-time code evaluation

### 📊 Advanced Analytics
- Performance metrics
- Learning pattern analysis
- Personalized recommendations

---

## 📂 Project Structure

```
interview-simulator/
├── src/
│   ├── app.py                     # Main application entry point
│   │   ├── InterviewSimulator     # Core simulator class
│   │   ├── conversation_memory    # Memory management
│   │   └── llm_integration        # LLM provider integration
│   │
│   └── vectordb.py                # Vector database operations
│       ├── DocumentProcessor      # Document processing and chunking
│       ├── VectorStore            # ChromaDB integration
│       └── Embeddings             # Embedding generation
│
├── data/                          # Knowledge base files
│   ├── backend.txt
│   ├── database.txt
│   ├── frontend.txt
│   ├── mern_integration.txt
│   ├── oop.txt
│   ├── software_architecture.txt
│   └── software_development_lifecycle.txt
│
├── requirements.txt               # Project dependencies
├── .env                           # Environment variables
├── .gitignore                     # Git ignore rules
├── LICENSE                        # MIT License
└── README.md                      # Documentation
```

---

## 🧱 Key Components

**src/app.py**
- Main application logic
- Interview simulation flow
- Conversation management
- LLM integration

**src/vectordb.py**
- Handles document processing and embeddings
- Performs semantic vector search using ChromaDB

**data/**
- Domain-specific structured knowledge base

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork this repository
2. Create a new feature branch
3. Commit your changes
4. Submit a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <b>🚀 Happy Interviewing!</b><br>
  <sub>Developed with ❤️ using RAG + LLMs</sub>
</p>
