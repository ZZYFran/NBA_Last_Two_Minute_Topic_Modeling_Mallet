import csv

TOPIC_LABELS = {
    0: "Close-range contact near the basket",
    1: "Shot attempt with incidental contact",
    2: "Replay review and ruling outcome",
    3: "Perimeter shot with defender contact",
    4: "Drive or shot contested by defender",
    5: "Screen-related offensive contact",
    6: "Off-ball or weak-side contact",
    7: "Post-play physical contact",
    8: "Marginal contact & non-call assessment",
    9: "Guard-driven shot with defensive pressure",
    10: "Wing isolation or drive play",
    11: "General shooting foul situation"
}


input_file = "doc-topics.txt"
output_file = "labelled_doc_topics.csv"

rows = []

with open(input_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue

        parts = line.strip().split()
        doc_name = parts[1]

        topic_pairs = parts[2:]
        for i in range(0, len(topic_pairs), 2):
            topic_id = int(topic_pairs[i])
            proportion = float(topic_pairs[i + 1])
            label = TOPIC_LABELS.get(topic_id, "UNKNOWN")

            rows.append([
                doc_name,
                topic_id,
                label,
                proportion
            ])


with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "document",
        "topic_id",
        "topic_label",
        "topic_proportion"
    ])
    writer.writerows(rows)

print(f"[DONE] Output written to {output_file}")
