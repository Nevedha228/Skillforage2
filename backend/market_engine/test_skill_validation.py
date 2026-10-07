from market_engine.skill_extractor import extract_skills
from market_engine.validation_data import VALIDATION_DATASET


# ============================================================
# SKILL EXTRACTION VALIDATION
# ============================================================


def calculate_metrics(
    true_positive,
    false_positive,
    false_negative
):
    """
    Calculate precision, recall and F1-score.
    """

    if true_positive + false_positive == 0:
        precision = 0.0
    else:
        precision = (
            true_positive /
            (true_positive + false_positive)
        )

    if true_positive + false_negative == 0:
        recall = 0.0
    else:
        recall = (
            true_positive /
            (true_positive + false_negative)
        )

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = (
            2 * precision * recall
        ) / (
            precision + recall
        )

    return (
        precision,
        recall,
        f1
    )


# ============================================================
# RUN VALIDATION
# ============================================================


def run_validation():

    total_true_positive = 0
    total_false_positive = 0
    total_false_negative = 0

    print("\n")
    print("=" * 60)
    print("SKILLFORAGE SKILL EXTRACTION VALIDATION")
    print("=" * 60)

    print(
        f"\nValidation jobs: "
        f"{len(VALIDATION_DATASET)}"
    )

    # ========================================================
    # PROCESS EACH JOB
    # ========================================================

    for job in VALIDATION_DATASET:

        job_id = job["id"]

        text = job["text"]

        expected = set(
            job["expected_skills"]
        )

        predicted = set(
            extract_skills(text)
        )

        true_positive = (
            expected &
            predicted
        )

        false_positive = (
            predicted -
            expected
        )

        false_negative = (
            expected -
            predicted
        )

        total_true_positive += len(
            true_positive
        )

        total_false_positive += len(
            false_positive
        )

        total_false_negative += len(
            false_negative
        )

        print("\n" + "-" * 60)

        print(
            f"{job_id}"
        )

        print(
            "Expected:",
            sorted(expected)
        )

        print(
            "Detected:",
            sorted(predicted)
        )

        print(
            "Correct:",
            sorted(true_positive)
        )

        print(
            "False Positive:",
            sorted(false_positive)
        )

        print(
            "Missed:",
            sorted(false_negative)
        )

    # ========================================================
    # FINAL METRICS
    # ========================================================

    precision, recall, f1 = calculate_metrics(
        total_true_positive,
        total_false_positive,
        total_false_negative
    )

    print("\n")
    print("=" * 60)
    print("FINAL VALIDATION RESULTS")
    print("=" * 60)

    print(
        f"\nTrue Positives : "
        f"{total_true_positive}"
    )

    print(
        f"False Positives: "
        f"{total_false_positive}"
    )

    print(
        f"False Negatives: "
        f"{total_false_negative}"
    )

    print(
        f"\nPrecision: "
        f"{precision * 100:.2f}%"
    )

    print(
        f"Recall: "
        f"{recall * 100:.2f}%"
    )

    print(
        f"F1-score: "
        f"{f1 * 100:.2f}%"
    )

    print("\n" + "=" * 60)


# ============================================================
# MAIN
# ============================================================


if __name__ == "__main__":

    run_validation()