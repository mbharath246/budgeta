from budgeta import settings
from langchain.embeddings.base import Embeddings
import httpx


class CohereEmbeddings(Embeddings):
    api_key = settings.COHERE_API_KEY
    model = settings.COHERE_EMBEDDINGS_MODEL
    input_type = settings.COHERE_EMBEDDINGS_INPUT_TYPE
    api_url = settings.COHERE_API_URL
    embedding_types: list = settings.COHERE_EMBEDDING_TYPE # float or int ....
    max_retries: int = settings.MAX_RETRIES
    
    def get_embeddings(self, texts: list[str]):
        i = 0
        while i < self.max_retries:
            try:
                with httpx.Client() as client:
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Accept":"application/json",
                        "content-type": "application/json"
                    }
                    data = {
                        "model": self.model,
                        "texts": texts,
                        "input_type": self.input_type,
                        "embedding_types": self.embedding_types
                    }
                    response = client.post(
                        url=self.api_url,
                        headers=headers,
                        json=data
                    )
                    response.raise_for_status()
                response = response.json()
                return response.get('embeddings', {}).get('float', [0.1])
            
            except Exception as e:
                print(f"Error While Embedding text {texts}: {e}")

            i += 1
            
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.get_embeddings(texts)
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        embeddings = self.get_embeddings([text])
        return embeddings[0]
    
    def get_embeddings_dimension(self):
        dimensions = self.embed_query("test_embeddings_size")
        return len(dimensions)    
    

embeddings = CohereEmbeddings()