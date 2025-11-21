"""
Retrieval Configuration Settings

This module contains all configurable parameters for the RAG retrieval system,
including chunking strategies, embedding models, and performance optimization settings.
"""

# Text Chunking Configuration
CHUNK_CONFIG = {
    "chunk_size": 500,                    # Characters per chunk
    "chunk_overlap": 50,                  # Overlap between chunks for context continuity
    "separators": [                       # Split priority (most to least preferred)
        "\n\n",                           # Paragraph breaks (highest priority)
        "\n",                             # Line breaks
        ". ",                             # Sentence endings
        ", ",                             # Commas
        " ",                              # Spaces
        ""                                # Individual characters (fallback)
    ]
}

# Vector Database Configuration
VECTORDB_CONFIG = {
    "collection_name": "rag_documents",   # ChromaDB collection name
    "persistence_path": "./chroma_db",    # Path to persist embeddings
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2"  # Default model
}

# Retrieval Search Configuration
SEARCH_CONFIG = {
    "default_top_k": 5,                   # Default number of results to return
    "max_top_k": 20,                      # Maximum allowed results
    "min_similarity_threshold": 0.3,      # Minimum similarity score (0-1)
    "distance_metric": "cosine"           # Distance metric for similarity
}

# Performance Metrics Configuration
METRICS_CONFIG = {
    "target_retrieval_latency_ms": 500,   # Target response time (milliseconds)
    "enable_performance_logging": True,   # Log retrieval performance metrics
    "enable_relevance_scoring": True,     # Calculate and store relevance scores
    "evaluation_batch_size": 10           # Batch size for evaluation queries
}

# Document Domain Configuration
DOMAIN_CONFIG = {
    "domains": [
        {
            "name": "Backend Development",
            "file": "backend.txt",
            "topics": ["APIs", "Server Architecture", "Protocols", "Performance"]
        },
        {
            "name": "Database Systems",
            "file": "database.txt",
            "topics": ["Data Modeling", "Query Optimization", "Indexing", "Transactions"]
        },
        {
            "name": "Frontend Development",
            "file": "frontend.txt",
            "topics": ["Frameworks", "UI/UX", "JavaScript", "Performance"]
        },
        {
            "name": "MERN Stack",
            "file": "mern_integration.txt",
            "topics": ["MongoDB", "Express", "React", "Node.js", "Full-stack"]
        },
        {
            "name": "Object-Oriented Programming",
            "file": "oop.txt",
            "topics": ["Design Patterns", "SOLID Principles", "Inheritance", "Polymorphism"]
        },
        {
            "name": "Software Architecture",
            "file": "software_architecture.txt",
            "topics": ["System Design", "Scalability", "Patterns", "Best Practices"]
        },
        {
            "name": "Software Development Lifecycle",
            "file": "software_development_lifecycle.txt",
            "topics": ["Methodologies", "Testing", "Deployment", "CI/CD"]
        }
    ],
    "default_domain_filter": None         # None = search all domains
}

# Interview Question Configuration
INTERVIEW_CONFIG = {
    "difficulty_levels": ["beginner", "intermediate", "advanced"],
    "default_difficulty": "intermediate",
    "context_window_size": 3,             # Number of previous Q&As to maintain
    "max_conversation_turns": 50          # Maximum interview length
}

# LLM Provider Configuration
LLM_CONFIG = {
    "provider_priority": [
        "openai",                         # Try OpenAI first if key available
        "groq",                           # Try Groq second
        "google"                          # Try Google third
    ],
    "openai": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 1024
    },
    "groq": {
        "model": "mixtral-8x7b-32768",
        "temperature": 0.7,
        "max_tokens": 1024
    },
    "google": {
        "model": "gemini-pro",
        "temperature": 0.7,
        "max_tokens": 1024
    }
}


def get_chunk_config():
    """Get text chunking configuration."""
    return CHUNK_CONFIG


def get_vectordb_config():
    """Get vector database configuration."""
    return VECTORDB_CONFIG


def get_search_config():
    """Get search/retrieval configuration."""
    return SEARCH_CONFIG


def get_metrics_config():
    """Get performance metrics configuration."""
    return METRICS_CONFIG


def get_domain_config():
    """Get domain configuration."""
    return DOMAIN_CONFIG


def get_interview_config():
    """Get interview configuration."""
    return INTERVIEW_CONFIG


def get_llm_config():
    """Get LLM provider configuration."""
    return LLM_CONFIG


def update_chunk_size(new_size: int):
    """Update chunk size dynamically."""
    CHUNK_CONFIG["chunk_size"] = new_size
    print(f"Chunk size updated to {new_size}")


def update_top_k(new_top_k: int):
    """Update default top-k results dynamically."""
    if new_top_k > SEARCH_CONFIG["max_top_k"]:
        print(f"Warning: top-k limited to maximum of {SEARCH_CONFIG['max_top_k']}")
        SEARCH_CONFIG["default_top_k"] = SEARCH_CONFIG["max_top_k"]
    else:
        SEARCH_CONFIG["default_top_k"] = new_top_k
    print(f"Default top-k updated to {SEARCH_CONFIG['default_top_k']}")
