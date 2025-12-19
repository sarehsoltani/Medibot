from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from typing import List
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceBgeEmbeddings

# Load PDF files from a directory
def load_pdf_files(data):
    loader = DirectoryLoader(
        data,
        glob = "*.pdf",
        loader_cls = PyPDFLoader)
    Documents = loader.load()
    
    return Documents    
    
# Filter documents to keep only page_content and source metadata
def filter_to_minimal_docs(documents: List[Document]) -> List[Document]:
    minimal_docs = []
    for doc in documents:
        src = doc.metadata.get("source", "unknown")
        minimal_docs.append(Document(page_content=doc.page_content, metadata={"source": src}))
    return minimal_docs    

# Split text into smaller chunks
def text_spliter(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

# Download the Embedding model
def download_embedding_model():
    embedder = HuggingFaceBgeEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedder

