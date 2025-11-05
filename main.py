import os
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

# Load the file from local directory
pdf_path = "HumanNutrition.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

print(f"Total pages loaded: {len(docs)}")
print(docs[0].page_content[:500])

# Clean text 
def clean_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
    text = re.sub(
        r'(\w)\s+(\w)',
        lambda m: m.group(1) + m.group(2)
        if m.group(1).islower() and m.group(2).islower()
        else m.group(1) + ' ' + m.group(2),
        text
    )
    return text.strip()

for d in docs:
    d.page_content = clean_text(d.page_content)

print("Text cleaning done.")

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)
chunks = splitter.split_documents(docs)
print(f"Total chunks created: {len(chunks)}")

# Create Vector embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# storing the embedding FAISS
db = FAISS.from_documents(chunks, embeddings)

# Create Retriever
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Load LLM 
llm = Ollama(model="tinyllama")

# Build RAG Chain 
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)


if __name__ == "__main__":
    query = "What are the main sources of Vitamin C?"
    result = qa_chain.invoke({"query": query})
    print("\nQuestion:", query)
    print("Answer:", result["result"])
