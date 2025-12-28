from django.conf import settings
from langchain.embeddings.base import Embeddings
import cohere


class CohereEmbeddings(Embeddings):
    api_key = settings.COHERE_API_KEY
    model = settings.COHERE_EMBEDDINGS_MODEL
    input_type = settings.COHERE_EMBEDDINGS_INPUT_TYPE
    cohere_client = None
    if settings.AI_ENABLED:
        cohere_client = cohere.ClientV2(api_key=api_key)
    
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        res = self.cohere_client.embed(
            texts=texts,
            model=self.model,
            input_type=self.input_type,
            embedding_types=["float"],
        )
        return res.embeddings.float

    def embed_query(self, text: str) -> list[float]:
        res = self.cohere_client.embed(
            texts=[text],
            model=self.model,
            input_type=self.input_type,
            embedding_types=["float"],
        )
        return res.embeddings.float[0]
    
    def get_embeddings_dimension(self):
        dimensions = self.embed_query("test_embeddings_size")
        return len(dimensions)    
    

embeddings = CohereEmbeddings()