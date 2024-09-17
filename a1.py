import os
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
import numpy as np
import re
import chromadb
import requests
import json

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')



#  load and chunk the .docx file
def load_and_chunk_docx(doc_name, max_chunk_size=5000):
   
    text = docx2txt.process(f"./input-docs/{doc_name}.docx")
    text = re.sub(r'\s+', ' ', text)
    sentences = sent_tokenize(text)
    current_chunk = ""
    chunks = []
    for sentence in sentences:
        if len(sentence) > max_chunk_size:
            # Split the long sentence into smaller parts
            for i in range(0, len(sentence), max_chunk_size):
                part_sentence = sentence[i:i + max_chunk_size]
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                chunks.append(part_sentence)
        else:
            # Check if adding the sentence exceeds the max_chunk_size
            if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                # Once the current chunk is full, add it to the list and start a new chunk
                chunks.append(current_chunk)
                current_chunk = sentence

    # Add the last chunk if any content is left
    if current_chunk:
        chunks.append(current_chunk)

    # Create overlapping chunks with a moving window (by 1 sentence each time)
    overlapping_chunks = []
    for i in range(len(chunks)):
        current_window = ""
        for j in range(i, len(sentences)):
            if len(current_window) + len(sentences[j]) + 1 <= max_chunk_size:
                current_window += " " + sentences[j] if current_window else sentences[j]
            else:
                break
        overlapping_chunks.append(current_window.strip())
    
    return overlapping_chunks

def expand_query(query):
    expanded_query = query
    words = query.split()
    
    for word in words:
        synonyms = wordnet.synsets(word)
        if synonyms:
            # Get a synonym if available
            synonym = synonyms[0].lemmas()[0].name()
            if synonym != word:
                expanded_query += f" {synonym}"
    
    return expanded_query


def vectorize_and_retrieve(chunks, query):
    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    doc_vectors = vectorizer.fit_transform(chunks)
    
    # Expand the query and vectorize it
    print(f"query: {query}")
    expanded_query = expand_query(query)
    print(f"expanded query: {expanded_query}")
    query_vector = vectorizer.transform([expanded_query])
    
    # Compute cosine similarity between the query and document chunks
    similarity_scores = cosine_similarity(query_vector, doc_vectors).flatten()
    
    # Retrieve the top matching chunk
    top_chunk_idx = np.argmax(similarity_scores)
    
    return chunks[top_chunk_idx], similarity_scores[top_chunk_idx]    



def query_document(query, chunks):
    url = "http://localhost:11434/api/generate"
    data = {
    "model": "llama3.1",
    "prompt": "Why is the sky blue?",
    "stream": False
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")




def main():
    docx_name = 'mog'
    chunks = load_and_chunk_docx(docx_name)
    query = input("Please input your query: ")
    most_similar_chunk, similarity =  vectorize_and_retrieve(chunks, query)
    print("most similar chunk to query:")
    print(most_similar_chunk)
    print(f"similarity: {similarity}")

if __name__ == "__main__":
    main()

