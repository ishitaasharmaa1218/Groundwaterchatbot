import os
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

# Load embeddings
def get_embeddings():
    return OpenAIEmbeddings()

# Create or load vectorstore
def get_vectorstore():
    embeddings = get_embeddings()

    if os.path.exists("vectorstore"):
        db = FAISS.load_local("vectorstore", embeddings)
    else:
        # Load your data
        loader = TextLoader("data/data.txt")  # make sure this file exists
        documents = loader.load()

        # Split text
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = splitter.split_documents(documents)

        # Create vectorstore
        db = FAISS.from_documents(docs, embeddings)

        # Save it
        db.save_local("vectorstore")

    return db

# Main chatbot function
def ask_bot(query):
    db = get_vectorstore()

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        retriever=db.as_retriever()
    )

    response = qa.run(query)
    return response