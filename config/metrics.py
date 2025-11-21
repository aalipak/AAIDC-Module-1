"""
Retrieval Evaluation Metrics Module

This module provides comprehensive metrics for evaluating the quality and performance
of the RAG retrieval system, including relevance scoring, coverage analysis, and latency tracking.
"""

import time
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import defaultdict


class RetrievalMetrics:
    """
    Comprehensive metrics collection and evaluation for retrieval quality.
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self.query_count = 0
        self.total_latency = 0
        self.latencies = []
        self.relevance_scores = []
        self.domain_coverage = defaultdict(int)
        self.chunk_hits = defaultdict(int)
        
    def record_query_latency(self, latency_ms: float):
        """Record query retrieval latency."""
        self.latencies.append(latency_ms)
        self.total_latency += latency_ms
        self.query_count += 1
        
    def record_relevance_scores(self, distances: List[float]):
        """Record relevance scores (cosine distances) from search results."""
        # Convert distance to similarity (1 - distance for cosine)
        similarities = [1 - d for d in distances]
        self.relevance_scores.extend(similarities)
        
    def record_domain_hit(self, domain_name: str, chunk_count: int = 1):
        """Record hit on a specific domain."""
        self.domain_coverage[domain_name] += chunk_count
        
    def record_chunk_hit(self, chunk_id: str):
        """Record that a specific chunk was retrieved."""
        self.chunk_hits[chunk_id] += 1
        
    def get_average_latency(self) -> float:
        """Get average retrieval latency in milliseconds."""
        if self.query_count == 0:
            return 0
        return self.total_latency / self.query_count
    
    def get_latency_percentiles(self) -> Dict[str, float]:
        """Get latency percentiles."""
        if not self.latencies:
            return {}
        return {
            "p50": np.percentile(self.latencies, 50),
            "p95": np.percentile(self.latencies, 95),
            "p99": np.percentile(self.latencies, 99),
            "min": min(self.latencies),
            "max": max(self.latencies)
        }
    
    def get_average_relevance_score(self) -> float:
        """Get average relevance (similarity) score."""
        if not self.relevance_scores:
            return 0
        return np.mean(self.relevance_scores)
    
    def get_top_k_precision(self, k: int = 5, threshold: float = 0.6) -> float:
        """
        Calculate Top-K Precision.
        Percentage of top-k results with relevance above threshold.
        """
        if not self.relevance_scores or len(self.relevance_scores) < k:
            return 0
        top_k_scores = sorted(self.relevance_scores, reverse=True)[:k]
        relevant_count = sum(1 for score in top_k_scores if score > threshold)
        return relevant_count / k
    
    def get_mean_reciprocal_rank(self, threshold: float = 0.6) -> float:
        """
        Calculate Mean Reciprocal Rank (MRR).
        Average of reciprocal ranks of first relevant result.
        """
        if not self.relevance_scores:
            return 0
        
        sorted_scores = sorted(self.relevance_scores, reverse=True)
        for rank, score in enumerate(sorted_scores, 1):
            if score > threshold:
                return 1 / rank
        return 0  # No relevant results found
    
    def get_domain_coverage(self) -> Dict[str, float]:
        """
        Get domain coverage distribution.
        Returns percentage of retrievals per domain.
        """
        total_hits = sum(self.domain_coverage.values())
        if total_hits == 0:
            return {}
        return {
            domain: (hits / total_hits) * 100 
            for domain, hits in self.domain_coverage.items()
        }
    
    def get_chunk_hit_distribution(self, top_n: int = 10) -> Dict[str, int]:
        """Get most frequently retrieved chunks."""
        return dict(sorted(
            self.chunk_hits.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_n])
    
    def get_retrieval_coverage(self, total_chunks: int) -> float:
        """
        Get retrieval coverage percentage.
        What percentage of total knowledge base chunks were touched.
        """
        if total_chunks == 0:
            return 0
        unique_chunks_hit = len(self.chunk_hits)
        return (unique_chunks_hit / total_chunks) * 100
    
    def get_context_coherence(self, retrieved_distances: List[List[float]]) -> float:
        """
        Calculate context coherence.
        Average similarity between retrieved chunks (how well they relate).
        """
        if not retrieved_distances or len(retrieved_distances) == 0:
            return 0
        
        coherences = []
        for distances in retrieved_distances:
            if len(distances) > 1:
                # Average of all pairwise similarities in result set
                similarities = [1 - d for d in distances]
                coherence = np.mean(similarities)
                coherences.append(coherence)
        
        return np.mean(coherences) if coherences else 0
    
    def get_redundancy_score(self, retrieved_distances: List[List[float]]) -> float:
        """
        Calculate redundancy score.
        Lower is better - indicates less duplicate/similar content.
        0 = no redundancy, 1 = high redundancy
        """
        if not retrieved_distances or len(retrieved_distances) == 0:
            return 0
        
        redundancies = []
        for distances in retrieved_distances:
            if len(distances) > 1:
                similarities = [1 - d for d in distances]
                # High similarity = high redundancy
                redundancy = np.mean(similarities)
                redundancies.append(redundancy)
        
        return np.mean(redundancies) if redundancies else 0
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive evaluation report."""
        return {
            "query_statistics": {
                "total_queries": self.query_count,
                "average_latency_ms": self.get_average_latency(),
                "latency_percentiles": self.get_latency_percentiles()
            },
            "relevance_metrics": {
                "average_relevance_score": self.get_average_relevance_score(),
                "top_5_precision": self.get_top_k_precision(k=5),
                "mean_reciprocal_rank": self.get_mean_reciprocal_rank()
            },
            "coverage_metrics": {
                "domain_coverage": self.get_domain_coverage(),
                "unique_chunks_hit": len(self.chunk_hits)
            },
            "sample_report": {
                "timestamp": time.time(),
                "metrics_collected": True
            }
        }
    
    def reset(self):
        """Reset all metrics."""
        self.query_count = 0
        self.total_latency = 0
        self.latencies = []
        self.relevance_scores = []
        self.domain_coverage = defaultdict(int)
        self.chunk_hits = defaultdict(int)


class RetrievalBenchmark:
    """
    Benchmark suite for evaluating retrieval quality against test queries.
    """
    
    def __init__(self, test_queries: List[str], expected_relevant_domains: Dict[str, List[str]]):
        """
        Initialize benchmark.
        
        Args:
            test_queries: List of test queries
            expected_relevant_domains: Dict mapping query index to list of relevant domains
        """
        self.test_queries = test_queries
        self.expected_relevant_domains = expected_relevant_domains
        self.results = []
    
    def evaluate_query(self, query_idx: int, retrieved_domains: List[str], 
                      relevance_scores: List[float]) -> Dict[str, Any]:
        """
        Evaluate a single query result.
        
        Returns:
            Evaluation metrics for the query
        """
        expected = set(self.expected_relevant_domains.get(query_idx, []))
        retrieved = set(retrieved_domains)
        
        # Calculate precision and recall
        if len(retrieved) == 0:
            precision = 0
        else:
            precision = len(expected & retrieved) / len(retrieved)
        
        if len(expected) == 0:
            recall = 1.0
        else:
            recall = len(expected & retrieved) / len(expected)
        
        # Calculate F1 score
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)
        
        evaluation = {
            "query_idx": query_idx,
            "query": self.test_queries[query_idx],
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "average_relevance": np.mean(relevance_scores) if relevance_scores else 0
        }
        
        self.results.append(evaluation)
        return evaluation
    
    def get_benchmark_summary(self) -> Dict[str, float]:
        """Get summary statistics across all evaluations."""
        if not self.results:
            return {}
        
        return {
            "mean_precision": np.mean([r["precision"] for r in self.results]),
            "mean_recall": np.mean([r["recall"] for r in self.results]),
            "mean_f1": np.mean([r["f1_score"] for r in self.results]),
            "mean_relevance": np.mean([r["average_relevance"] for r in self.results]),
            "queries_evaluated": len(self.results)
        }
