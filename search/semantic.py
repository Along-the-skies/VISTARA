import numpy as np
from models.all_MiniLM_L6_v2.model import model



def generate_embedding(text, batch_size=32):
    return model.embed(text)


def embedding_to_blob(embedding):
    return np.asarray(embedding, dtype=np.float32).tobytes()