"""
Configuration package for Interview Simulator RAG system.

Includes:
- Retrieval configuration (chunking, search parameters)
- Performance metrics collection and evaluation
- Interview settings
- LLM provider configuration
"""

from .retrieval_config import (
    get_chunk_config,
    get_vectordb_config,
    get_search_config,
    get_metrics_config,
    get_domain_config,
    get_interview_config,
    get_llm_config,
    update_chunk_size,
    update_top_k
)

from .metrics import RetrievalMetrics, RetrievalBenchmark

__all__ = [
    "get_chunk_config",
    "get_vectordb_config",
    "get_search_config",
    "get_metrics_config",
    "get_domain_config",
    "get_interview_config",
    "get_llm_config",
    "update_chunk_size",
    "update_top_k",
    "RetrievalMetrics",
    "RetrievalBenchmark"
]
