import docx2txt


def preprocess_document(document_path):
    text = docx2txt.process(document_path)
    chunks = []
    

    return text

def main():
    document_path = "input-docs/mog.docx"
    query = "What is the termination clause in this contract?"

    # Preprocess the document
    document_text = preprocess_document(document_path)

    print("document text:")
    print(document_text)

if __name__ == "__main__":
    main()