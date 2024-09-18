import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
import numpy as np
import re
import requests
import json

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')



#  load and chunk the .docx file

'''
This splits the document text into sentences. It then creates chunks <= 5000 characters
which contain either a single part of a sentence or one or more whole sentences. That is,
sentences are not split accross chunks so that the LLM has coherent english to work with.
It first creates non-overlapping chunks then takes these chunks and implements a rolling window
of one sentence so that all subsequences of sentences are captured. This will increase the
likelyhood that the appropriate context will be supplied to the LLM.
'''
def load_and_chunk_docx(doc_name, max_chunk_size=5000):
   
    text = docx2txt.process(f"./input-docs/{doc_name}.docx")
    text = re.sub(r'\s+', ' ', text) #remove large spaces
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


'''
This a simple query expansion technique that will add synonyms of words contained in the
query. This will increase the recall rate of the sparse search. This would not add much if
any value if a dense search was being done with a decent embedding model since the model
could be expected to match synonyms as well as exact matches.
'''
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



'''
Sparse Search: Generate TF-IDF vectors for the chunks and query.
Then select the most similar chunk vector to the query vector
using the cosine similarity metric. The idea is that the chunk
selected will be most similar to the query + synonyms in terms
of words that appear in both but are less common in all of the 
chunks taken together.
'''
def vectorize_and_retrieve(chunks, query):
    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    doc_vectors = vectorizer.fit_transform(chunks)
    
    # Expand the query and vectorize it
    expanded_query = expand_query(query)
    print(f"expanded query: {expanded_query}")
    query_vector = vectorizer.transform([expanded_query])
    
    # Compute cosine similarity between the query and document chunks
    similarity_scores = cosine_similarity(query_vector, doc_vectors).flatten()
    
    # Retrieve the top matching chunk
    top_chunk_idx = np.argmax(similarity_scores)
    
    
    return chunks[top_chunk_idx], similarity_scores[top_chunk_idx]    


'''
Pass the query and most similar chunk to the LLM together. 
'''
def query_document(query, chunk):
    url = "http://192.168.137.2:11434/api/generate"
    prompt = f"""
    You are a legal assistant. A user is asking a question about the content of a legal contract.
    Use the following contract text to answer the question truthfully. If you do not know the answer, say so.
    In your answer only use the content of the Contract Text provided.

    Contract Text:
    {"".join(chunk)}

    Question: {query}
    Answer:
    """
    data = {
    "model": "llama3.1",
    "prompt": prompt,
    "stream": False,
    "temperature": 0
    }

    headers = {
        'Content-Type': 'application/json'
    }

    print(f"\nprompt being sent: {prompt}\n")

    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        return json.loads(response.text)["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"



def answer_is_hallucination(chunk, query, answer):
    # Technique 1: Simple keyword matching for grounding
    keywords = query.split()  # Use query terms as a simple heuristic
    if not any(keyword.lower() in chunk.lower() for keyword in keywords):
        return True

    # Technique 2: Confidence scoring using cosine similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([chunk, answer])
    similarity_score = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    if similarity_score < 0.1:  # Arbitrary low threshold to detect potential hallucinations
        return True
    
    return False


def main():
    docx_name = 'mog'
    chunks = load_and_chunk_docx(docx_name)
    query = input("Please input your query: ")
    most_similar_chunk, similarity =  vectorize_and_retrieve(chunks, query)
    print(f"similarity: {similarity}")
    response = query_document(query, most_similar_chunk)
    print(f"Model Response: ")
    if answer_is_hallucination(most_similar_chunk, query, response):
        print("Note: this answer may be a hallucination: ")
    print(response)
    

if __name__ == "__main__":
    main()

