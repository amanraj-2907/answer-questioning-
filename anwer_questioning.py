from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain
import os


os.environ["HUGGINGFACEHUB_API_TOKEN"] = "YOUR_HF_TOKEN_HERE"  


def load_document(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents


def split_text_into_chunks(documents, chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def create_vector_store(chunks, embeddings):
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings)
    return vectorstore


def process_document(file_path):
    documents = load_document(file_path)
    chunks = split_text_into_chunks(documents)
    embeddings = create_embeddings()
    vectorstore = create_vector_store(chunks, embeddings)
    return vectorstore


def ask_question(vectorstore, question):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)

    llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5, "max_length": 100})
    chain = load_qa_chain(llm, chain_type="stuff")
    answer = chain.run(input_documents=docs, question=question)
    return answer


if __name__ == "__main__":
    file_path = "C:/Users/Asus/OneDrive/ドキュメント/India is a South Asian country with its capital in New Delhi.pdf"  # Apna path daalna
    vectorstore = process_document(file_path)
    print(" Document processed and stored in vectorstore.")

    question = "What is the capital of India?"  
    answer = ask_question(vectorstore, question)
    print(" Answer:", answer)
