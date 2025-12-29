# Medibot: LLM-Powered Medical Chatbot

**Medibot** is a Generative AI chatbot designed to assist with medical queries. It utilizes **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware answers based on a curated knowledge base of medical PDF documents. 

By leveraging **LangChain**, **Pinecone**, and **OpenAI**, Medibot enables users to chat conversationally with medical literature, maintaining context across multiple turns of conversation.

## 🚀 Features

- **RAG Architecture**: Retrieves relevant medical context from a vector database before generating answers to ensure accuracy and reduce hallucinations.
- **Conversational Memory**: Remembers previous questions and context within a session, allowing for follow-up questions.
- **Vector Search**: Uses Pinecone for high-performance similarity search on document embeddings.
- **Automated Deployment**: Integrated CI/CD pipeline using GitHub Actions for seamless updates to AWS EC2.

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Framework**: Flask (Web Application)
- **Orchestration**: LangChain (v0.3.x)
- **Vector Database**: Pinecone
- **LLM**: OpenAI (GPT-3.5/4)
- **Embeddings**: Sentence Transformers / HuggingFace
- **DevOps**: AWS EC2, GitHub Actions, Docker (optional if used)

## 📂 Project Structure

```text
Medibot/
├── .github/
│   └── workflows/
│       └── main.yml     # CI/CD Pipeline configuration
├── src/
│   ├── helper.py        # Functions for loading and splitting PDFs
│   ├── prompt.py        # Prompt templates for system instructions
│   └── ...
├── templates/
│   └── chat.html        # HTML frontend for the chatbot
├── static/              # CSS/JS files
├── store_index.py       # Script to ingest PDFs into Pinecone
├── app.py               # Main Flask application
├── requirements.txt     # Python dependencies
├── .env                 # API keys (not uploaded to GitHub)
└── README.md


⚙️ Installation (Local)

1. Clone the repository: 

```bash
git clone https://github.com/sarehsoltani/Medibot.git
```
### 2. Create a Virtual Environment

```bash
conda create -n medibot python=3.10 -y
```

```bash
conda activate medibot
```


### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables: 
Create a `.env` file in the root directory and add your Pinecone & Huggingface credentials as follows:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
HUGGINGFACE_TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

🧠 Data Ingestion
Before running the chatbot, you need to process your medical PDFs:

Place your PDF files in the data/ directory.

Run the ingestion script:

```bash
# run the following command to store embeddings to pinecone
python store_index.py
```

```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up localhost:
```


# 🔄 CI/CD Deployment
This project uses GitHub Actions for Continuous Integration and Deployment to AWS EC2.

## 1. Login to AWS console.

## 2. Create IAM user for deployment

	#with specific access

	1. EC2 access : It is virtual machine

	2. ECR: Elastic Container registry to save your docker image in aws


	#Description: About the deployment

	1. Build docker image of the source code

	2. Push your docker image to ECR

	3. Launch Your EC2 

	4. Pull Your image from ECR in EC2

	5. Lauch your docker image in EC2

	#Policy:

	1. AmazonEC2ContainerRegistryFullAccess

	2. AmazonEC2FullAccess

	
## 3. Create ECR repo to store/save docker image
    - Save the URI: 802249258227.dkr.ecr.us-east-1.amazonaws.com/medicalbot

## 4. Create EC2 machine (Ubuntu) 

## 5. Open EC2 and Install docker in EC2 Machine:
	
	#optinal

	sudo apt-get update -y

	sudo apt-get upgrade
	
	#required

	curl -fsSL https://get.docker.com -o get-docker.sh

	sudo sh get-docker.sh

	sudo usermod -aG docker ubuntu

	newgrp docker
	
# 6. Configure EC2 as self-hosted runner:
    setting>actions>runner>new self hosted runner> choose os> then run command one by one


# 7. Setup github secrets:

   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - ECR_REPO
   - PINECONE_API_KEY
   - OPENAI_API_KEY



