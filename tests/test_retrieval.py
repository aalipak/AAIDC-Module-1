"""
Test suite for retrieval metrics and evaluation.

Tests retrieval quality, performance metrics, and benchmark evaluation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.metrics import RetrievalMetrics, RetrievalBenchmark
import numpy as np


def test_retrieval_metrics():
    """Test basic metrics collection."""
    metrics = RetrievalMetrics()
    
    # Test latency recording
    metrics.record_query_latency(100.5)
    metrics.record_query_latency(150.2)
    metrics.record_query_latency(120.0)
    
    avg_latency = metrics.get_average_latency()
    assert abs(avg_latency - 123.57) < 1, f"Expected ~123.57, got {avg_latency}"
    print("✓ Latency recording works correctly")
    
    # Test latency percentiles
    percentiles = metrics.get_latency_percentiles()
    assert "p50" in percentiles
    assert "p95" in percentiles
    assert "p99" in percentiles
    print("✓ Latency percentiles calculated correctly")


def test_relevance_metrics():
    """Test relevance scoring."""
    metrics = RetrievalMetrics()
    
    # Record distances (lower is better in cosine distance)
    distances = [0.1, 0.2, 0.15, 0.25, 0.3]
    metrics.record_relevance_scores(distances)
    
    # Average similarity should be high (1 - low distances)
    avg_relevance = metrics.get_average_relevance_score()
    assert 0.8 < avg_relevance < 0.95, f"Expected 0.8-0.95, got {avg_relevance}"
    print("✓ Relevance scoring works correctly")
    
    # Test precision
    precision = metrics.get_top_k_precision(k=5, threshold=0.6)
    assert 0 <= precision <= 1, f"Precision should be 0-1, got {precision}"
    print("✓ Top-K precision calculation works")


def test_domain_coverage():
    """Test domain coverage metrics."""
    metrics = RetrievalMetrics()
    
    # Record hits from different domains
    metrics.record_domain_hit("Backend", 10)
    metrics.record_domain_hit("Database", 8)
    metrics.record_domain_hit("Frontend", 7)
    
    coverage = metrics.get_domain_coverage()
    assert abs(coverage["Backend"] - 38.46) < 1, "Backend coverage incorrect"
    assert abs(coverage["Database"] - 30.77) < 1, "Database coverage incorrect"
    assert abs(coverage["Frontend"] - 26.92) < 1, "Frontend coverage incorrect"
    print("✓ Domain coverage calculation works correctly")


def test_chunk_retrieval():
    """Test chunk retrieval tracking."""
    metrics = RetrievalMetrics()
    
    # Record multiple chunk retrievals
    for i in range(5):
        metrics.record_chunk_hit(f"chunk_0_{i}")
    
    metrics.record_chunk_hit("chunk_0_0")  # Hit same chunk twice
    metrics.record_chunk_hit("chunk_0_0")
    
    unique_chunks = len(metrics.chunk_hits)
    assert unique_chunks == 5, f"Expected 5 unique chunks, got {unique_chunks}"
    
    # Check most hit chunk
    most_hit = metrics.get_chunk_hit_distribution(top_n=1)
    assert most_hit["chunk_0_0"] == 3, "Most hit chunk should have 3 hits"
    print("✓ Chunk retrieval tracking works correctly")


def test_context_coherence():
    """Test context coherence calculation."""
    metrics = RetrievalMetrics()
    
    # Simulate highly coherent results (small distances = high similarity)
    coherent_distances = [[0.05, 0.08, 0.06, 0.07, 0.09]]  # Very similar chunks
    coherence = metrics.get_context_coherence(coherent_distances)
    
    assert 0.85 < coherence < 1.0, f"Coherent results should be 0.85-1.0, got {coherence}"
    print("✓ Context coherence calculation works correctly")


def test_redundancy_score():
    """Test redundancy score calculation."""
    metrics = RetrievalMetrics()
    
    # Simulate high redundancy (all chunks very similar)
    redundant_distances = [[0.02, 0.03, 0.02, 0.04, 0.03]]
    redundancy = metrics.get_redundancy_score(redundant_distances)
    
    assert 0.95 < redundancy < 1.0, f"High redundancy should be 0.95-1.0, got {redundancy}"
    
    # Simulate low redundancy (diverse chunks)
    diverse_distances = [[0.4, 0.5, 0.45, 0.55, 0.6]]
    redundancy = metrics.get_redundancy_score(diverse_distances)
    
    assert 0.3 < redundancy < 0.7, f"Low redundancy should be 0.3-0.7, got {redundancy}"
    print("✓ Redundancy score calculation works correctly")


def test_retrieval_coverage():
    """Test retrieval coverage percentage."""
    metrics = RetrievalMetrics()
    
    # Hit 40 unique chunks out of 100 total
    for i in range(40):
        metrics.record_chunk_hit(f"chunk_{i}")
    
    coverage = metrics.get_retrieval_coverage(total_chunks=100)
    assert abs(coverage - 40.0) < 0.1, f"Expected 40%, got {coverage}%"
    print("✓ Retrieval coverage calculation works correctly")


def test_benchmark_evaluation():
    """Test benchmark evaluation suite."""
    test_queries = [
        "What is OOP?",
        "How to optimize queries?",
        "Explain MERN stack"
    ]
    
    expected_domains = {
        0: ["OOP", "Patterns"],
        1: ["Database", "Performance"],
        2: ["MERN", "Backend", "Frontend"]
    }
    
    benchmark = RetrievalBenchmark(test_queries, expected_domains)
    
    # Evaluate query 0
    retrieved_domains = ["OOP", "Patterns", "Backend"]
    relevance_scores = [0.9, 0.85, 0.6]
    result = benchmark.evaluate_query(0, retrieved_domains, relevance_scores)
    
    assert result["precision"] > 0.6, "Precision should be high"
    assert result["recall"] == 1.0, "Recall should be perfect (all expected found)"
    print("✓ Benchmark evaluation works correctly")


def test_metrics_report():
    """Test comprehensive metrics report generation."""
    metrics = RetrievalMetrics()
    
    # Add sample data
    for i in range(10):
        metrics.record_query_latency(100 + i * 5)
        metrics.record_relevance_scores([0.1 + i * 0.02, 0.15 + i * 0.02])
        metrics.record_domain_hit("Backend", 1)
        metrics.record_chunk_hit(f"chunk_{i}")
    
    report = metrics.generate_report()
    
    assert "query_statistics" in report
    assert "relevance_metrics" in report
    assert "coverage_metrics" in report
    assert report["query_statistics"]["total_queries"] == 10
    print("✓ Comprehensive metrics report generated successfully")


def test_metrics_reset():
    """Test metrics reset functionality."""
    metrics = RetrievalMetrics()
    
    # Add data
    metrics.record_query_latency(100)
    metrics.record_relevance_scores([0.1, 0.2])
    metrics.record_domain_hit("Backend", 5)
    
    # Reset
    metrics.reset()
    
    assert metrics.query_count == 0, "Query count should be 0 after reset"
    assert len(metrics.latencies) == 0, "Latencies should be empty after reset"
    assert len(metrics.relevance_scores) == 0, "Relevance scores should be empty after reset"
    print("✓ Metrics reset works correctly")


def run_all_tests():
    """Run all test cases."""
    print("\n" + "="*50)
    print("Running Retrieval Metrics Tests")
    print("="*50 + "\n")
    
    tests = [
        test_retrieval_metrics,
        test_relevance_metrics,
        test_domain_coverage,
        test_chunk_retrieval,
        test_context_coherence,
        test_redundancy_score,
        test_retrieval_coverage,
        test_benchmark_evaluation,
        test_metrics_report,
        test_metrics_reset
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
