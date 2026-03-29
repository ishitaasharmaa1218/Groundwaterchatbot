import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import pipeline

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vectorstore/index.faiss")

with open("vectorstore/texts.txt", "r", encoding="utf-8") as f:
    texts = f.readlines()

generator = pipeline(
    "text-generation",
    model="google/flan-t5-base"
)

def ask_bot(question):

    query_embedding = model.encode([question])

    distances, indices = index.search(np.array(query_embedding), k=3)

    context = ""
    for i in indices[0]:
        context += texts[i]

    prompt = f"""
    You are a groundwater analysis assistant.

    Context:
    {context}

    Question: {question}

    Give a clear explanation of the groundwater trend.
    """

    result = generator(prompt, max_length=200)

    answer = result[0]["generated_text"]

    return answer, context