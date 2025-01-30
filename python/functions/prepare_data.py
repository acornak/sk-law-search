import docx
import re

law_number_pattern = re.compile(r'^\d{3}/\d{4}\s+Z\. z\.', re.MULTILINE)
section_pattern = re.compile(
    r'^\s*(Základné zásady|Prvá|Druhá|Tretia|Štvrtá|Piatá|Šiesta|Siedma|Ôsma|Deviata|Desiata|Jedenásta|Dvanástá|Trinástá|Štrnástá|Pätnástá|Šestnástá|Sedemnástá|Osemnástá|Devätnástá|Dvadsiata)\s+ČASŤ\b.*$', 
    re.IGNORECASE | re.MULTILINE
)
article_pattern = re.compile(
    r'^\s*Čl\.\s*\d+\b.*$', 
    re.IGNORECASE | re.MULTILINE
)
paragraph_pattern = re.compile(
    r'^\s*§\s*\d+\b.*$', 
    re.IGNORECASE | re.MULTILINE
)

def load_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        stripped_text = para.text.lstrip()  # Remove leading whitespace
        if stripped_text:  # Ensure the paragraph is not empty after stripping
            text += stripped_text + "\n\n"
    return text


def extract_law_metadata(text):
    law_number_match = re.search(r'(\d{3}/\d{4})\s+Z\. z\.', text)
    date_match = re.search(r'z\s+(\d{1,2}\.\s+\w+\s+\d{4})', text)
    law_number = law_number_match.group(1) if law_number_match else "Unknown"
    date = date_match.group(1) if date_match else "Unknown"
    return {"law_number": law_number, "date": date}


def split_into_sections(text):
    sections = []
    section_matches = list(section_pattern.finditer(text))
    print(f"Found {len(section_matches)} sections")
    for i, match in enumerate(section_matches):
        section_title = match.group(1)
        start = match.end()
        end = section_matches[i + 1].start() if i + 1 < len(section_matches) else len(text)
        section_content = text[start:end].strip()
        sections.append({"section_title": section_title, "content": section_content})
    return sections


def split_into_articles(section_content):
    articles = []
    article_matches = list(article_pattern.finditer(section_content))
    if not article_matches:
        # If no articles, treat the entire section as one article
        articles.append({"article_title": "No Article", "content": section_content})
        return articles
    for i, match in enumerate(article_matches):
        article_title = match.group()
        start = match.end()
        end = article_matches[i + 1].start() if i + 1 < len(article_matches) else len(section_content)
        article_content = section_content[start:end].strip()
        articles.append({"article_title": article_title, "content": article_content})
    return articles


def split_into_paragraphs(article_content):
    paragraphs = []
    paragraph_matches = list(paragraph_pattern.finditer(article_content))
    
    if not paragraph_matches:
        # If no paragraphs, treat the entire article as one paragraph
        paragraphs.append({"paragraph_title": "No Paragraph", "content": article_content})
        return paragraphs
    
    for i, match in enumerate(paragraph_matches):
        paragraph_title = match.group()
        start = match.end()
        end = paragraph_matches[i + 1].start() if i + 1 < len(paragraph_matches) else len(article_content)
        paragraph_content = article_content[start:end].strip()
        paragraphs.append({"paragraph_title": paragraph_title, "content": paragraph_content})
    
    return paragraphs


def parse_document(text):
    # save text to .txt file
    with open("text.txt", "w") as f:
        f.write(text)

    law_metadata = extract_law_metadata(text)
    sections = split_into_sections(text)

    print(f"Extracted metadata: {law_metadata}")
    print(f"Extracted {len(sections)} sections")
    
    parsed_data = []
    
    for section in sections:
        section_title = section['section_title']
        articles = split_into_articles(section['content'])
        
        for article in articles:
            article_title = article['article_title']
            paragraphs = split_into_paragraphs(article['content'])
            
            for paragraph in paragraphs:
                paragraph_title = paragraph['paragraph_title']
                content = paragraph['content']
                
                # Avoid empty content
                if content:
                    parsed_data.append({
                        "law_number": law_metadata['law_number'],
                        "date": law_metadata['date'],
                        "section": section_title,
                        "article": article_title,
                        "paragraph": paragraph_title,
                        "content": content
                    })
    
    return parsed_data
