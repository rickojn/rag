import os
import docx

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)




text = extract_text_from_docx("input-docs/Employment-Contract-08-21-01.docx")
print(text )