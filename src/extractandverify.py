import re, json, requests
import pandas as pd
from rapidfuzz import process
from tqdm import tqdm

RAW_FILE = "reddit_booksuggestions_cleaned.json"



with open(RAW_FILE, "r", encoding="utf-8") as f:
    posts = json.load(f)

QUOTED = re.compile(r"[\"“”'’‘](.+?)[\"“”'’‘]")
BY_AUTHOR = re.compile(r"(.+?)\s+by\s+[\w\s\.\-']{2,}", re.I)
CAP_TITLE = re.compile(r"\b([A-Z][\w'\-]*(?:\s+[A-Z][\w'\-]*){1,5})")

def harvest_titles(text):
    titles = set()
    titles.update(QUOTED.findall(text))
    titles.update(BY_AUTHOR.findall(text))
    if not titles:
        titles.update(CAP_TITLE.findall(text))
    return [
        t.strip() for t in titles
        if 2 <= len(t.split()) <= 10 and len(t) <= 100
    ]

candidates = []
for i, post in enumerate(posts):
    keyword = post.get("keyword", "")
    post_id = post.get("post_id", "")

    for comment in post.get("comments", []):
        if not isinstance(comment, dict):
            continue
        text = comment.get("text", "").strip()
        sentiment = comment.get("sentiment", 0.0)
        upvotes = comment.get("upvotes", 0)

        for title in harvest_titles(text):
            candidates.append({
                "title_raw": title,
                "comment": text,
                "sentiment": sentiment,
                "upvotes": upvotes,
                "keyword": keyword,
                "post_index": i,
                "post_id": post_id
            })

print(f"🔍 Found {len(candidates)} candidate titles")


books_df = pd.read_csv("books.csv")  # from goodbooks-10k
known_titles = books_df["title"].dropna().unique()


verified = []
known_titles = books_df["title"].dropna().unique()
for entry in tqdm(candidates, desc="Offline Match"):
    match, score, _ = process.extractOne(entry["title_raw"], known_titles)
    if score >= 91:  
        match_row = books_df[books_df["title"] == match]
        if not match_row.empty:
            author = match_row.iloc[0]["authors"]
            year = match_row.iloc[0]["original_publication_year"]
        else:
            author = "Unknown"
        entry["verified_title"] = match
        entry["match_score"] = score
        entry["author"] = author
        entry["year"] = year
        verified.append(entry)

print(f" Verified {len(verified)} titles with offline dataset")

# === Save ===
pd.DataFrame(verified).to_csv("verified_books_offline.csv", index=False, encoding="utf-8")
with open("verified_books_offline.json", "w", encoding="utf-8") as f:
    json.dump(verified, f, ensure_ascii=False, indent=2)

print("Saved verified results to CSV and JSON")
