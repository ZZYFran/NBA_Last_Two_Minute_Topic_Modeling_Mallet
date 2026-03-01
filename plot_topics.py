import pandas as pd
import matplotlib.pyplot as plt


INPUT = "labelled_doc_topics.csv"

df = pd.read_csv(INPUT)

df["doc_file"] = df["document"].str.replace("file:", "", regex=False).str.split("/").str[-1]


dominant = (
    df.sort_values(["doc_file", "topic_proportion"], ascending=[True, False])
      .groupby("doc_file", as_index=False)
      .head(1)
      .reset_index(drop=True)
)

dominant_out = dominant[["doc_file", "topic_id", "topic_label", "topic_proportion"]].copy()
dominant_out = dominant_out.sort_values("topic_proportion", ascending=False)
dominant_out.to_csv("dominant_topics_per_doc.csv", index=False)
print("[DONE] Saved dominant_topics_per_doc.csv")

topic_counts = dominant["topic_label"].value_counts().sort_values(ascending=False)

plt.figure()
topic_counts.plot(kind="bar")
plt.ylabel("Number of documents (dominant topic)")
plt.xlabel("Topic label")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("topic_counts.png", dpi=200)
print("[DONE] Saved topic_counts.png")

avg_share = (
    df.groupby(["topic_id", "topic_label"], as_index=False)["topic_proportion"]
      .mean()
      .sort_values("topic_proportion", ascending=False)
)

plt.figure()
plt.bar(avg_share["topic_label"], avg_share["topic_proportion"])
plt.ylabel("Average topic proportion across documents")
plt.xlabel("Topic label")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("topic_avg_share.png", dpi=200)
print("[DONE] Saved topic_avg_share.png")


print("\nTop 10 dominant topics by frequency:")
print(topic_counts.head(10).to_string())

print("\nTop 10 documents with strongest dominance (highest proportion):")
print(dominant_out.head(10).to_string(index=False))
