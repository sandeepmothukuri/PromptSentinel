"""
Attack simulation benchmark — measures detection rates, false positives, and throughput.

Usage:
    python benchmarks/run_benchmarks.py
    python benchmarks/run_benchmarks.py --format json
    python benchmarks/run_benchmarks.py --category injection
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

# Ensure repository root is on sys.path when executed directly
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from promptsentinel.scanner import Scanner  # noqa: E402

DATASETS = _REPO_ROOT / "attacks" / "datasets"


def load_dataset(name: str) -> list[dict]:
    path = DATASETS / f"{name}_attacks.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def run(dataset_name: str, scanner: Scanner) -> dict:
    cases = load_dataset(dataset_name)
    if not cases:
        return {}

    tp = fp = tn = fn = 0
    latencies: list[float] = []
    misses: list[dict] = []
    false_alarms: list[dict] = []

    for case in cases:
        t0 = time.perf_counter()
        report = scanner.scan(case["text"])
        latency_ms = (time.perf_counter() - t0) * 1000
        latencies.append(latency_ms)

        expected = case.get("expected_detector")
        detected = bool(report.findings)

        if expected is None:
            if detected:
                fp += 1
                false_alarms.append({"id": case["id"], "text": case["text"][:80]})
            else:
                tn += 1
        else:
            if detected:
                tp += 1
            else:
                fn += 1
                misses.append({"id": case["id"], "text": case["text"][:80], "expected": expected})

    total = tp + fp + tn + fn
    precision = tp / (tp + fp) if (tp + fp) else 1.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    avg_ms = sum(latencies) / len(latencies) if latencies else 0

    return {
        "dataset": dataset_name,
        "total_cases": total,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "detection_rate": round(recall * 100, 1),
        "precision": round(precision * 100, 1),
        "f1_score": round(f1 * 100, 1),
        "false_positive_rate": round(fp / (fp + tn) * 100, 1) if (fp + tn) else 0.0,
        "avg_latency_ms": round(avg_ms, 3),
        "misses": misses,
        "false_alarms": false_alarms,
    }


def print_report(results: list[dict]) -> None:
    print("\n" + "=" * 70)
    print("  promptsentinel - Attack Detection Benchmark Report")
    print("=" * 70)
    for r in results:
        if not r:
            continue
        print(f"\n  Dataset     : {r['dataset']}")
        print(f"  Total cases : {r['total_cases']}")
        print(f"  Detection   : {r['detection_rate']}%  (recall)")
        print(f"  Precision   : {r['precision']}%")
        print(f"  F1 Score    : {r['f1_score']}%")
        print(f"  False +rate : {r['false_positive_rate']}%")
        print(f"  Avg latency : {r['avg_latency_ms']} ms/scan")
        if r["misses"]:
            print(f"\n  Missed detections ({len(r['misses'])}):")
            for m in r["misses"]:
                print(f"    [{m['id']}] {m['text']}")
        if r["false_alarms"]:
            print(f"\n  False positives ({len(r['false_alarms'])}):")
            for fa in r["false_alarms"]:
                print(f"    [{fa['id']}] {fa['text']}")
    print("\n" + "=" * 70 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run promptsentinel detection benchmarks")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--category", choices=["injection", "jailbreak", "all"], default="all")
    args = parser.parse_args()

    scanner = Scanner()
    datasets = ["injection", "jailbreak"] if args.category == "all" else [args.category]

    results = [run(d, scanner) for d in datasets]

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print_report(results)


if __name__ == "__main__":
    main()
