# 🤖 AI Interview Simulator and Feedback System

## 📚 Overview

This is an intelligent RAG-based (Retrieval-Augmented Generation) AI system designed to simulate technical interviews and provide detailed feedback. The system uses a comprehensive knowledge base covering various software development topics to conduct realistic interview simulations and offer constructive feedback.

## 🎯 Key Features

- 🗣️ **Interactive Interview Simulation**
  - Conducts natural, context-aware technical interviews
  - Maintains conversation memory for follow-up questions
  - Adapts difficulty based on responses

- 📚 **Comprehensive Knowledge Base**
  - Software Development Life Cycle (SDLC)
  - Object-Oriented Programming (OOP)
  - Backend Development
  - Frontend Development
  - Database Systems
  - Software Architecture
  - MERN Stack Integration

- � **Smart Feedback System**
  - Provides detailed feedback on technical accuracy
  - Suggests areas for improvement
  - Offers relevant resources for learning
  - Maintains context across the interview session

## �️ Technical Implementation

### Architecture

The system is built using a RAG (Retrieval-Augmented Generation) architecture:

1. **Document Processing**
   - Loads technical interview content from structured text files
   - Chunks content into manageable pieces
   - Creates embeddings for efficient retrieval

2. **Vector Database**
   - Uses ChromaDB for storing document embeddings
   - Enables semantic search across the knowledge base
   - Maintains conversation history for context

3. **LLM Integration**
   - Supports multiple LLM providers (OpenAI, Groq, Google)
   - Uses custom prompts for interview simulation
   - Maintains conversation context for natural flow


### Knowledge Base Structure

```
data/
├── backend.txt          # Backend development concepts
├── database.txt        # Database systems and design
├── frontend.txt        # Frontend development topics
├── mern_integration.txt # MERN stack implementation
├── oop.txt             # Object-oriented programming
├── software_architecture.txt # System design principles
└── software_development_lifecycle.txt # SDLC processes
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- One of the following API keys:
  - OpenAI API key
  - Groq API key
  - Google AI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone [your-repo-url]
   cd interview-simulator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key:**
   Create a `.env` file and add your chosen API key:
   ```env
   OPENAI_API_KEY=your_key_here
   # or
   GROQ_API_KEY=your_key_here
   # or
   GOOGLE_API_KEY=your_key_here
   ```

## 🔄 Conversation Flow

1. **Interview Initiation**
   - System loads domain knowledge
   - Establishes initial conversation context
   - Sets interview difficulty level

2. **Question Generation**
   - Dynamic question selection based on topic
   - Adaptive difficulty based on responses
   - Context-aware follow-up questions

3. **Response Analysis**
   - Technical accuracy verification
   - Concept understanding assessment
   - Knowledge depth evaluation

4. **Feedback Generation**
   - Detailed technical feedback
   - Improvement suggestions
   - Resource recommendations
   - Progress tracking

## 📈 Future Enhancements

1. **Extended Knowledge Base**
   - More technical domains
   - Updated best practices
   - Industry-specific content

2. **Enhanced Interaction**
   - Mock coding exercises
   - System design challenges
   - Real-time code evaluation

3. **Advanced Analytics**
   - Performance metrics
   - Learning pattern analysis
   - Personalized recommendations

## 📂 Project Structure

```
interview-simulator/
├── src/
│   ├── app.py                 # Main application entry point
│   │   ├── InterviewSimulator # Core simulator class
│   │   ├── conversation_memory # Memory management
│   │   └── llm_integration    # LLM provider integration
│   │
│   └── vectordb.py           # Vector database operations
│       ├── DocumentProcessor  # Document processing and chunking
│       ├── VectorStore       # ChromaDB integration
│       └── Embeddings        # Embedding generation
│
├── data/                     # Knowledge base
│   ├── backend.txt          # Backend development
│   ├── database.txt         # Database systems
│   ├── frontend.txt         # Frontend development
│   ├── mern_integration.txt # MERN stack
│   ├── oop.txt             # OOP concepts
│   ├── software_architecture.txt  # Architecture
│   └── software_development_lifecycle.txt  # SDLC
│
│
├── requirements.txt         # Project dependencies
├── .env          # Environment 
├── .gitignore             # Git ignore rules
├── LICENSE                # MIT License
└── README.md             # Documentation
```

### Key Components

1. **src/app.py**
   - Main application logic
   - Interview simulation flow
   - Conversation management
   - LLM integration

2. **src/vectordb.py**
   - Document processing
   - Vector database operations
   - Embedding generation
   - Semantic search

3. **data/**
   - Technical knowledge base
   - Structured text documents
   - Domain-specific content

4. **tests/**
   - Unit tests
   - Integration tests
   - Test fixtures and utilities

5. **config/**
   - LLM configuration
   - System settings
   - Interview prompts

## 🤝 Contributing

We welcome contributions to improve the interview simulator! Please feel free to:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Happy Interviewing! 🚀**
