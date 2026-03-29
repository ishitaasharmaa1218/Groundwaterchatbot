from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def ask_bot(query):
    response = generator(query, max_length=100, num_return_sequences=1)
    return response[0]['generated_text'], ""