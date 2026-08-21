import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text, batch_size=32):
    return model.encode(
        text,
        batch_size=batch_size,
        show_progress_bar=False
    )


def embedding_to_blob(embedding):
    return np.asarray(embedding, dtype=np.float32).tobytes()