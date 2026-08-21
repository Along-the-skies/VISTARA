from pathlib import Path
from docx import Document

def extract_text(path:Path) -> str:
    try:
        document = Document(path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text:
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)
    except Exception:
        return ""