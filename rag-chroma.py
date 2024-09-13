import os
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import docx
import chromadb


def extract_paragraphs_from_docx(docx_path):
    doc = docx.Document(docx_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return full_text

def embed_and_store_paragraphs(paragraphs, collection):
    # collection.add(paragraphs)
    collection.add(documents = paragraphs,
                   ids = paragraphs)

def retrieve_most_relevant_paragraph(query, collection):
    return collection.query(
        query_texts = [query],
        n_results = 2
    )


chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection("paragraphs")

paragraphs = extract_paragraphs_from_docx("input-docs/Employment-Contract-08-21-01.docx")
unique_paragraphs = list(set(paragraphs))
embed_and_store_paragraphs(unique_paragraphs, collection)
query = "what sick pay is available?"
results = retrieve_most_relevant_paragraph(query, collection)

print(results)
