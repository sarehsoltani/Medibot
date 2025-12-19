import os
from dotenv import load_dotenv
from src.helper import load_pdf_files, filter_to_minimal_docs, text_spliter, download_embedding_model
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore


# Load environment variables from .env file
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN


extracted_data = load_pdf_files("data")
filtered_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_spliter(filtered_data)

embedding_model = download_embedding_model()

# Initialize Pinecone

pinecone_api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone_api_key)
index_name = "medical-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embedding_model,
    index_name= index_name
)


