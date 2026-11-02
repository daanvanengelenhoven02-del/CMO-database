"""Reads approved rows from the published Google Sheet and writes data/entries.json
with one embedding per Context, Mechanism and Outcome narrative."""
import json, os
import pandas as pd
from sentence_transformers import SentenceTransformer

df = pd.read_csv(os.environ["SHEET_CSV_URL"])
df.columns = [c.strip() for c in df.columns]
df = df[df["Approved"].astype(str).str.strip().str.lower() == "yes"].reset_index(drop=True)

FIELDS = ["Context", "Mechanism", "Outcome"]
model = SentenceTransformer("intfloat/multilingual-e5-small")
emb = {f: model.encode(["passage: " + str(t) for t in df[f].fillna("")], normalize_embeddings=True)
       for f in FIELDS}

entries = []
for i, r in df.iterrows():
    entries.append({
        "title": str(r["Title"]), "description": str(r["Description"]), "link": str(r["Link"]),
        **{f.lower(): str(r[f]) for f in FIELDS},
        "emb": {f.lower(): [round(float(x), 4) for x in emb[f][i]] for f in FIELDS},
    })

os.makedirs("data", exist_ok=True)
with open("data/entries.json", "w", encoding="utf-8") as fh:
    json.dump(entries, fh, ensure_ascii=False)
print(f"Wrote {len(entries)} entries")
