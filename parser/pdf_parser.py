from pathlib import Path
from pypdf import PdfReader

def extract_text(path:Path) -> str:
    try:
        reader = PdfReader(path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)
    except Exception:
        return ""