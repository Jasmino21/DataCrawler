import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]
embed_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)




index = pc.Index(host="https://fbpostsindex-0i28dvm.svc.aped-4627-b74a.pinecone.io")


# 2. Embed the question
embedded_query = embed_model.embed_query("Suggest jobs for Python developer, Web Developer, Data Scientist, Machine Learning Engineer")

# 3. Query Pinecone
results = index.query(
    namespace="__default__",
    vector=embedded_query, 
    top_k=10,
    include_metadata=True,
    include_values=False
)

print(results)