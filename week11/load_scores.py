import csv

def load_scores(file):
    kept = []
    skipped = []

    with open(file, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = (row.get("name") or "").strip()
            score_text = (row.get("score") or "").strip()

            try:
                score = int(score_text)
            except (ValueError, TypeError):
                skipped.append((name, score_text))
                continue

            if name and 0 <= score <= 100:
                kept.append((name, score))
            else:
                skipped.append((name, score))

    return kept, skipped