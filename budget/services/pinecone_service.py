import requests
from budgeta import settings
from langchain_core.documents import Document

if settings.AI_ENABLED:
    from budget.services.embeddings import embeddings


class PineconeService:
    def __init__(self):
        self.index_name = settings.PINECONE_INDEX_NAME
        self.top_k = settings.PINECONE_TOP_K
        self.payload_text = "text"

        self.api_key = settings.PINECONE_API_KEY
        self.control_plane = "https://api.pinecone.io"

        self.headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Pinecone-Api-Version": "2025-10",
        }

        self.index_host = self.get_or_create_index()

    def get_or_create_index(self):
        r = requests.get(
            f"{self.control_plane}/indexes",
            headers=self.headers,
            timeout=10,
        )
        r.raise_for_status()

        indexes = r.json().get("indexes", [])
        for idx in indexes:
            if idx["name"] == self.index_name:
                print("index found")
                return f"https://{idx['host']}"

        payload = {
            "name": self.index_name,
            "dimension": embeddings.get_embeddings_dimension(),
            "metric": "cosine",
            "vector_type": "dense",
            "spec": {
                "serverless": {
                    "cloud": "aws",
                    "region": "us-east-1",
                }
            },
        }
        print("Index Not Found Creating!...")

        r = requests.post(
            f"{self.control_plane}/indexes",
            headers=self.headers,
            json=payload,
            timeout=10,
        )
        r.raise_for_status()

        return f"https://{r.json()['host']}"

    def store_items(self, doc_id, texts: list[str], metadatas: list[dict]):
        embeddings_list = embeddings.embed_documents(texts)

        vectors = []
        for text, vector, metadata in zip(texts, embeddings_list, metadatas):
            metadata[self.payload_text] = text
            vectors.append({
                "id": str(doc_id),
                "values": vector,
                "metadata": metadata,
            })

        payload = {"vectors": vectors}

        r = requests.post(
            f"{self.index_host}/vectors/upsert",
            headers=self.headers,
            json=payload,
            timeout=15,
        )
        r.raise_for_status()

        print("Added data into Pinecone")

    def delete_item(self, doc_id):
        payload = {"ids": [str(doc_id)]}

        r = requests.post(
            f"{self.index_host}/vectors/delete",
            headers=self.headers,
            json=payload,
            timeout=10,
        )
        r.raise_for_status()

        print(f"Deleted vector {doc_id}")


    def search_points(self, query: str, user_id: str):
        vector = embeddings.embed_query(query)

        payload = {
            "vector": vector,
            "topK": self.top_k,
            "includeMetadata": True,
            "includeValues": False,
            "filter": {
                "user_id": {"$eq": str(user_id)}
            }
        }

        r = requests.post(
            f"{self.index_host}/query",
            headers=self.headers,
            json=payload,
            timeout=15,
        )
        r.raise_for_status()

        matches = r.json().get("matches", [])

        results = []
        for match in matches:
            metadata = match.get("metadata", {})
            page_content = metadata.pop(self.payload_text, "")
            metadata["score"] = match.get("score")

            results.append(
                Document(page_content=page_content)
                # or Document(page_content=page_content, metadata=metadata)
            )

        print(f"Found {len(results)} chunks from Pinecone")
        return results
        
