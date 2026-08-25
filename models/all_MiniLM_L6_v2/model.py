from pathlib import Path

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

from config import MODEL_PATH, TOKENIZER_PATH

class LocalEmbeddingModel:
    def __init__(self):
        self.tokenizer = Tokenizer.from_file(str(TOKENIZER_PATH))

        self.session = ort.InferenceSession(
            str(MODEL_PATH),
            providers=["CPUExecutionProvider"],
        )

    def embed(self,text:str) ->np.ndarray:
        encoded = self.tokenizer.encode(text)

        input_ids=np.array(
            [encoded.ids],
            dtype=np.int64,
        )

        attention_mask = np.array(
            [encoded.attention_mask],
            dtype=np.int64
        )

        token_type_ids = np.zeros_like(input_ids)

        outputs = self.session.run(
            None,
            {
                "input_ids": input_ids,
                "attention_mask":attention_mask,
                "token_type_ids":token_type_ids
            },
        )

        token_embeddings = outputs [0]
        mask = attention_mask.astype(np.float32)
        mask = np.expand_dims(mask,axis=-1)

        summed = np.sum(token_embeddings * mask,axis = 1)
        counts = np.clip(np.sum(mask,axis=1),1e-9,None)

        embedding = summed / counts

        embedding /= np.linalg.norm(
            embedding,
            axis=1,
            keepdims=True
        )

        return embedding[0]

model = LocalEmbeddingModel()