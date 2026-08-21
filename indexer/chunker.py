def chunk_text(content):
    words = content.split()

    chunks = []

    for start in range(0,len(words),500):
        chunk = words[start:start + 500]
        chunk= " ".join(chunk)
        chunks.append(chunk)

    return chunks