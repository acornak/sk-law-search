from functions.prepare_data import load_docx, parse_document


if __name__ == "__main__":
    file_path: str = "../data/ZZ_2003_595.docx"
    document_text = load_docx(file_path)

    parsed_documents = parse_document(document_text)
    for doc in parsed_documents[:10]:
        print(f"Law Number: {doc['law_number']}")
        print(f"Date: {doc['date']}")
        print(f"Section: {doc['section']}")
        print(f"Article: {doc['article']}")
        print(f"Paragraph: {doc['paragraph']}")
        print(f"Content: {doc['content'][:100]}...\n")

