import csv
from collections import defaultdict
import os

INPUT_CSV = "all_games.csv"
OUTPUT_DIR = "docs"


COMMENT_COL_CANDIDATES = ["comment"]
GAMEID_COL_CANDIDATES = ["game_id"]

def pick_col(fieldnames, candidates):
    for c in candidates:
        if c in fieldnames:
            return c
    return None

def main():
    if not os.path.exists(INPUT_CSV):
        print(f"[ERROR] Cannot find {INPUT_CSV} in current directory: {os.getcwd()}")
        print("Run: pwd && ls -lah  (and ensure all_games.csv is here)")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    docs = defaultdict(list)
    total_rows = 0
    empty_comment = 0

    with open(INPUT_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        print(f"[INFO] Detected columns ({len(fieldnames)}): {fieldnames[:20]}{' ...' if len(fieldnames)>20 else ''}")

        comment_col = pick_col(fieldnames, COMMENT_COL_CANDIDATES)
        gameid_col = pick_col(fieldnames, GAMEID_COL_CANDIDATES)

        if not comment_col:
            print("[ERROR] Cannot find a comment column. Candidates:", COMMENT_COL_CANDIDATES)
            return
        if not gameid_col:
            print("[ERROR] Cannot find a game_id column. Candidates:", GAMEID_COL_CANDIDATES)
            return

        print(f"[INFO] Using comment column: {comment_col}")
        print(f"[INFO] Using game id column: {gameid_col}")

        for row in reader:
            total_rows += 1
            comment = (row.get(comment_col) or "").strip()
            game_id = (row.get(gameid_col) or "").strip()

            if not comment:
                empty_comment += 1
                continue
            if not game_id:
                # 没有 game_id 的行就跳过，避免生成奇怪文件名
                continue

            docs[game_id].append(comment)

    for game_id, comments in docs.items():
        path = os.path.join(OUTPUT_DIR, f"{game_id}.txt")
        with open(path, "w", encoding="utf-8") as out:
            out.write(" ".join(comments))

    print(f"[DONE] Read rows: {total_rows}")
    print(f"[DONE] Empty comments: {empty_comment}")
    print(f"[DONE] Created documents: {len(docs)} in ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
