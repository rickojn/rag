import os
import docx
from sentence_transformers import SentenceTransformer, util

def extract_paragraphs_from_docx(docx_path):
    doc = docx.Document(docx_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return full_text

def embed_paragraphs(paragraphs, model):
    return model.encode(paragraphs, convert_to_tensor = True)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
paragraphs = extract_paragraphs_from_docx("input-docs/Employment-Contract-08-21-01.docx")

paragraph_embeddings = embed_paragraphs(paragraphs, model)

print(paragraphs[0])
print(paragraph_embeddings[0].shape())




