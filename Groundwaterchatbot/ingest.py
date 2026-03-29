import csv
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []

with open("data/groundwater_data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)

    for row in reader:
        text = " | ".join(f"{headers[i]}: {row[i]}" for i in range(len(headers)))
        texts.append(text)

embeddings = model.encode(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

os.makedirs("vectorstore", exist_ok=True)

faiss.write_index(index, "vectorstore/index.faiss")

with open("vectorstore/texts.txt", "w", encoding="utf-8") as f:
    for t in texts:
        f.write(t + "\n")

print("Vector database created.")