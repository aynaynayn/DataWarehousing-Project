import json

RAW_FILE = "reddit_booksuggestions_non_relational.json"
CLEAN_FILE = "reddit_booksuggestions_cleaned.json"

with open(RAW_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)


    



def is_valid_comment(text):
    text = text.strip()
    return (
        len(text) >= 10 and
        text.lower() not in {"[deleted]", "[removed]"}
    )

def clean_post(post):
    post["title"] = post["title"].strip()
    post["keyword"] = post["keyword"].strip().lower()

    cleaned_comments = []
    seen_texts = set()

    for c in post["comments"]:
        text = c.get("text", "").strip()

        if is_valid_comment(text) and text not in seen_texts:
            cleaned_comments.append({
                "comment_id": c.get("comment_id"),
                "text": text,
                "upvotes": c.get("upvotes", 0),
                "sentiment": c.get("sentiment", 0.0)
            })
            seen_texts.add(text)

    post["comments"] = cleaned_comments
    post["num_comments"] = len(cleaned_comments)

    return post if cleaned_comments else None

cleaned = [p for p in (clean_post(p) for p in data) if p]


with open(CLEAN_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print(f"Cleaned {len(cleaned)} posts — saved to {CLEAN_FILE}")
