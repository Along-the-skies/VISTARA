import numpy as np

def cosine_similarity(a,b):
    a = np.asarray(a, dtype=np.float32)
    b= np.asarray(b,dtype=np.float32)

    denominator = np.linalg.norm(a) * np.linalg.norm(b)

    if denominator == 0:
        return 0.0

    return float(np.dot(a, b) / denominator)