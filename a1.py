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





def main():
    docx_name = 'mog'
    query = 'What is the termination clause in this contract?'
    chunks = load_and_chunk_docx(docx_name)
    print("chunks: ")
    for index, chunk in enumerate(chunks):
        print(f"chunk{index}")
        print(chunk)


if __name__ == "__main__":
    main()

