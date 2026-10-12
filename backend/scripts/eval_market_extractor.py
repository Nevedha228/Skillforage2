import sys
from pathlib import Path
import json

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from market_engine.validation_data import VALIDATION_DATASET
from market_engine.skill_extractor import extract_skills

def evaluate_extractor():
    print(f"============================================================")
    print(f" SKILLFORAGE MARKET INTELLIGENCE — SKILL EXTRACTION BENCHMARK")
    print(f" Dataset: {len(VALIDATION_DATASET)} Hand-Labeled Job Postings")
    print(f"============================================================\n")

    total_tp = 0
    total_fp = 0
    total_fn = 0

    per_job_results = []

    for item in VALIDATION_DATASET:
        job_id = item["id"]
        text = item["text"]
        expected = set(s.lower().strip() for s in item["expected_skills"])

        # Extract skills using word-boundary taxonomy matcher
        extracted_raw = extract_skills(text)
        extracted = set(s.lower().strip() for s in extracted_raw)

        tp = len(expected.intersection(extracted))
        fp = len(extracted - expected)
        fn = len(expected - extracted)

        total_tp += tp
        total_fp += fp
        total_fn += fn

        p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0

        per_job_results.append({
            "id": job_id,
            "expected_count": len(expected),
            "extracted_count": len(extracted),
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "precision": round(p, 3),
            "recall": round(r, 3),
            "f1": round(f1, 3)
        })

    # Overall Micro-Averaged Metrics
    overall_precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
    overall_recall = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
    overall_f1 = (
        (2 * overall_precision * overall_recall) / (overall_precision + overall_recall)
        if (overall_precision + overall_recall) > 0 else 0.0
    )

    print(f"RESULTS SUMMARY:")
    print(f"------------------------------------------------------------")
    print(f" Total Hand-Labeled Jobs Evaluated: {len(VALIDATION_DATASET)}")
    print(f" True Positives (TP):               {total_tp}")
    print(f" False Positives (FP):              {total_fp}")
    print(f" False Negatives (FN):              {total_fn}")
    print(f" Micro Precision:                   {overall_precision:.4f} ({overall_precision * 100:.1f}%)")
    print(f" Micro Recall:                      {overall_recall:.4f} ({overall_recall * 100:.1f}%)")
    print(f" Micro F1 Score:                    {overall_f1:.4f} ({overall_f1 * 100:.1f}%)")
    print(f"------------------------------------------------------------\n")

    # Save reproducible evaluation results
    report = {
        "evaluation_timestamp": "2026-10-11T19:00:00Z",
        "total_test_samples": len(VALIDATION_DATASET),
        "true_positives": total_tp,
        "false_positives": total_fp,
        "false_negatives": total_fn,
        "precision": round(overall_precision, 4),
        "recall": round(overall_recall, 4),
        "f1_score": round(overall_f1, 4),
        "per_sample_metrics": per_job_results
    }

    report_path = BACKEND_DIR / "data" / "extraction_evaluation_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Full benchmark report saved to {report_path.name}")
    return report

if __name__ == "__main__":
    evaluate_extractor()
