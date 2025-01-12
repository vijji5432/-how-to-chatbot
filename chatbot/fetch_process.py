import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import spacy
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize the sentence transformer model to get embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Documentation URLs for each platform
doc_urls = {
    "Segment": "https://segment.com/docs/?ref=nav",
    "mParticle": "https://docs.mparticle.com/",
    "Lytics": "https://docs.lytics.com/",
    "Zeotap": "https://docs.zeotap.com/home/en-us/"
}

# Function to clean HTML content
def clean_html_content(raw_html):
    soup = BeautifulSoup(raw_html, "html.parser")
    for tag in soup(["script", "style", "header", "footer", "nav"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())

# Function to fetch documentation for a platform and create an index
def fetch_documentation(platform, max_depth=2):
    start_url = doc_urls.get(platform)
    if not start_url:
        return {"error": f"Documentation for {platform} is not available."}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    visited = set()
    content_store = {}
    queue = [(start_url, 0)]  # To simulate BFS
    while queue:
        current_url, depth = queue.pop(0)
        if depth > max_depth or current_url in visited:
            continue
        visited.add(current_url)

        try:
            print(f"Fetching: {current_url}")  # Debugging line to ensure scraping is working
            response = requests.get(current_url, headers=headers)
            response.raise_for_status()
            raw_content = response.content

            cleaned_content = clean_html_content(raw_content)
            content_store[current_url] = cleaned_content

            soup = BeautifulSoup(raw_content, "html.parser")
            for link in soup.find_all("a", href=True):
                link_url = urljoin(current_url, link["href"])
                if link_url not in visited:
                    queue.append((link_url, depth + 1))

        except Exception as e:
            print(f"Error fetching {current_url}: {e}")

    # Now, index the documents into FAISS
    index, doc_embeddings = index_documents(content_store)
    return content_store, index, doc_embeddings

# Function to create FAISS index
def index_documents(content_store):
    docs = list(content_store.values())
    # Convert documents to embeddings using the pre-trained model
    doc_embeddings = model.encode(docs)
    
    # Dimension of the embeddings
    dim = doc_embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)  # L2 distance for similarity search
    index.add(np.array(doc_embeddings, dtype=np.float32))  # Add embeddings to FAISS index
    
    return index, doc_embeddings

# Function to search for relevant documents using FAISS
def search_documents(index, query):
    # Convert the query into an embedding
    query_embedding = model.encode([query])
    
    # Search for the top 3 most similar documents
    D, I = index.search(np.array(query_embedding, dtype=np.float32), k=3)
    
    return I[0]  # Return the indices of the most similar documents

# Main function to fetch and match based on query
def fetch_and_match(query, platform):
    content_store, index, doc_embeddings = fetch_documentation(platform)

    if isinstance(content_store, dict) and "error" in content_store:
        return content_store

    # Use FAISS to find the most similar documents
    relevant_indices = search_documents(index, query)

    # Prepare the response using the most similar documents
    relevant_content = {}
    for idx in relevant_indices:
        url = list(content_store.keys())[idx]  # Map index back to URL
        relevant_content[url] = content_store[url][:500]  # Limit content length to 500 chars for readability

    return relevant_content if relevant_content else {"error": "No relevant content found."}

# BERT-based question answering function (if needed for deeper content matching)
def get_bert_answer(query, context):
    tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

    inputs = tokenizer.encode_plus(query, context, add_special_tokens=True, return_tensors='pt')
    answer_start_scores, answer_end_scores = model(**inputs)
    answer_start = torch.argmax(answer_start_scores)
    answer_end = torch.argmax(answer_end_scores)
    answer_tokens = inputs['input_ids'][0][answer_start:answer_end + 1]
    return tokenizer.decode(answer_tokens)
