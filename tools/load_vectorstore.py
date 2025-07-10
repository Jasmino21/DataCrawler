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
embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)
existing_indexes = [i["name"] for i in pc.list_indexes()]

# Delete existing index if it exists
# if PINECONE_INDEX_NAME in existing_indexes:
#     print(f"Deleting existing index: {PINECONE_INDEX_NAME}")
#     pc.delete_index(name=PINECONE_INDEX_NAME)
#     while PINECONE_INDEX_NAME in pc.list_indexes():
#         time.sleep(5)

# pc.create_index(
#     name=PINECONE_INDEX_NAME,
#     dimension=768,  # For GoogleGenerativeAI embeddings
#     metric="dotproduct",
#     spec=spec
# )
# while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
#     time.sleep(1)

# index = pc.Index(PINECONE_INDEX_NAME)
index = pc.Index(host="https://fbpostsindex-0i28dvm.svc.aped-4627-b74a.pinecone.io")

# Load, split, embed and upsert PDF content
def load_vectorstore():

     # Fetch fb_posts.json 
    fb_posts_path = 'output/fb_posts.json'
    
    with open(fb_posts_path, "r", encoding="utf-8") as f:
        fb_posts = json.load(f)

    today = time.strftime("%Y-%m-%d")
    fb_docs = []
    for idx, (post_author, post) in enumerate(fb_posts.items()):
        # get desc1, desc2, desc3, desc4 and compare which one has the most content
        desc_fields = [post.get("desc1", ""), post.get("desc2", ""), post.get("desc3", ""), post.get("desc4", "")]
        # Choose the one with the most non-whitespace characters
        description = max(desc_fields, key=lambda d: len(d.strip()))
        if not description.strip():
            description = 'No Content Available'
        fb_docs.append({
            "id": f"{idx}",
            "post_author": post_author,
            "post_desc": description,
            "post_date": today,
            "post_link": post.get("post_link", ""),
            "page_url": post.get("page_url", "")
        })

    #  Ingest
    texts = [doc["post_desc"] for doc in fb_docs]
    metadatas = fb_docs
    ids = [doc["id"] for doc in fb_docs]

    print(f"Embedding {len(texts)} chunks...")
    embeddings = embed_model.embed_documents(texts)

    print("Uploading to Pinecone...")
    with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
        index.upsert(vectors=zip(ids, embeddings, metadatas))
        progress.update(len(embeddings))

    print("Upload complete for fb_docs")

# load_vectorstore()
# 2. Embed the question
embedded_query = embed_model.embed_query("𝗦𝗣𝗖𝗖 𝗤𝘂𝗲𝘇𝗼𝗻 𝗖𝗶𝘁𝘆 𝗖𝗮𝗺𝗽𝘂𝘀 𝗶𝘀 𝗛𝗶𝗿𝗶𝗻𝗴")

# 3. Query Pinecone
results = index.query(
    namespace="__default__",
    vector=embedded_query, 
    top_k=60,
    include_metadata=True,
    include_values=False
)

print(results)