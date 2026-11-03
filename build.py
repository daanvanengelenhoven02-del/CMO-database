"""Reads approved rows from the published Google Sheet and writes data/entries.json
with one embedding per narrative field (Context, Parties involved, Mechanism, Outcome)."""
import json, os
import pandas as pd
from sentence_transformers import SentenceTransformer

df = pd.read_csv(os.environ["SHEET_CSV_URL"])
df.columns = [c.strip() for c in df.columns]

# sheet column -> key used on the website
FIELDS = {"Context": "context", "Parties involved": "parties",
          "Mechanism": "mechanism", "Outcome": "outcome"}
needed = ["Title", "Description", "Link", "Name of the article", "Approved", *FIELDS]
missing = [c for c in needed if c not in df.columns]
if missing:
    raise SystemExit(f"Missing columns: {missing}. The sheet has: {list(df.columns)}")

df = df[df["Approved"].astype(str).str.strip().str.lower() == "yes"].reset_index(drop=True)
df = df.fillna("")

model = SentenceTransformer("intfloat/multilingual-e5-small")
emb = {col: model.encode(["passage: " + str(t) for t in df[col]], normalize_embeddings=True)
       for col in FIELDS}


# "About" part: title + description, used only by the free-text search
about_emb = model.encode(["passage: " + str(t) + ". " + str(d) for t, d in zip(df["Title"], df["Description"])],
                         normalize_embeddings=True)
entries = []
for i, r in df.iterrows():
    entries.append({
        "title": str(r["Title"]), "description": str(r["Description"]),
        "link": str(r["Link"]), "article": str(r["Name of the article"]),
        **{key: str(r[col]) for col, key in FIELDS.items()},
        "emb": {**{key: [round(float(x), 4) for x in emb[col][i]] for col, key in FIELDS.items()},
                "about": [round(float(x), 4) for x in about_emb[i]]},,
    })

os.makedirs("data", exist_ok=True)
with open("data/entries.json", "w", encoding="utf-8") as fh:
    json.dump(entries, fh, ensure_ascii=False)
print(f"Wrote {len(entries)} entries")
