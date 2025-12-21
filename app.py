from flask import Flask, request, jsonify, render_template
from src.helper import download_embedding_model
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os


app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN

embedding_model = download_embedding_model()

index_name = "medical-chatbot"
# Embed each chunk and store in pinecone index
docsearch = PineconeVectorStore.from_existing_index(
    embedding=embedding_model,
    index_name=index_name
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Initialize the LLM
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.2",
    temperature=0,
    huggingfacehub_api_token=os.getenv("HUGGINGFACE_API_TOKEN"),
)

chat_model = ChatHuggingFace(llm=llm)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]    
)

question_answer_chain = create_stuff_documents_chain(chat_model, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods= ["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    response = rag_chain.invoke({"input": input})
    print("Response:", response["answer"])
    return str(response["answer"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port= 8080, debug= True)

