import docx2txt
import nltk
import re


# Define functions for preprocessing and querying
def preprocess_document(document_path):
    """Preprocesses a .docx document for RAG."""
    text = docx2txt.process(document_path)
    # # Remove punctuation and stop words
    # text = re.sub(r'[^\w\s]', '', text)
    # text = nltk.word_tokenize(text)
    # text = [word.lower() for word in text if word not in nltk.corpus.stopwords.words('english')]
    return text

def query_document(document_text, query):
    """Queries the preprocessed document using RAG."""
    # Split the document into chunks
    chunk_size = 500
    chunks = [document_text[i:i+chunk_size] for i in range(0, len(document_text), chunk_size)]

    # Create embeddings for chunks and query
    embeddings = []
    for chunk in chunks:
        response = openai.Embedding.create(
            input=chunk,
            model="text-embedding-ada-002"
        )
        embeddings.append(response.data[0].embedding)

    query_embedding = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )

    # Find the most similar chunk to the query
    most_similar_chunk = max(chunks, key=lambda x: openai.Embedding.similarity(query_embedding.data[0].embedding, x.embedding))

    # Generate a response using the most similar chunk
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Answer the question based on the following text:\n{most_similar_chunk}\n\nQuestion: {query}",
        temperature=0.5
    )

    return response.choices[0].text

# Mitigate hallucinations:
def query_expansion(query):
    """Expands the query using synonyms."""
    # Use a synonym database or API to find synonyms
    synonyms = ["synonym1", "synonym2", "synonym3"]
    expanded_query = query + " " + " ".join(synonyms)
    return expanded_query

def response_verification(response, document_text):
    """Verifies the response against the document text."""
    # Check if the response is consistent with the document content
    # Use keyword matching or semantic similarity to assess consistency
    # ... implementation omitted for brevity
    return True

# Main function
def main():
    document_path = "input-docs/gov.docx"
    query = "What is the termination clause in this contract?"

    # Preprocess the document
    document_text = preprocess_document(document_path)

    print("document text:")
    print(document_text)

    # # Expand the query
    # expanded_query = query_expansion(query)

    # # Query the document
    # response = query_document(document_text, expanded_query)

    # # Verify the response
    # is_verified = response_verification(response, document_text)

    # if is_verified:
    #     print("Response:", response)
    # else:
    #     print("Response could not be verified.")

if __name__ == "__main__":
    main()