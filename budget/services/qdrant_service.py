from qdrant_client.models import PayloadSchemaType
from langchain_core.documents import Document
from django.conf import settings
import logging as logger
import requests


if settings.AI_ENABLED:
    from budget.services.embeddings import embeddings


class QdrantService:
    qdrant_api_key = settings.QDRANT_API_KEY
    qdrant_url = settings.QDRANT_URL
    collection_name = settings.QDRANT_COLLECTION
    qdrant_client = None
    headers = {
        "api-key": qdrant_api_key,
        "Content-Type": "application/json"
    }

    def __init__(self):    
        if settings.AI_ENABLED:
            self.check_or_create_collection()               
            self.check_or_create_index('id', PayloadSchemaType.INTEGER.value)
            self.check_or_create_index('user_id', PayloadSchemaType.UUID.value)


    def check_or_create_collection(self):
        r = requests.get(
            url=self.qdrant_url + f"/collections/{self.collection_name}/exists",
            headers=self.headers
        )
        response = r.json()
        collection_exists = response.get('result', {}).get('exists')
        if not collection_exists:
            r = requests.put(
                url=self.qdrant_url + f"/collections/{self.collection_name}",
                headers=self.headers,
                json={
                    "vectors": {
                        "dense_vector": {
                        "size": embeddings.get_embeddings_dimension(),
                        "distance": "Cosine"
                        }
                    }
                }
            )
            res = r.json()
            print(f"Collection with name {self.collection_name} not Exists, Creating.., result: {res.get('result')}")
            logger.info(f"Collection with name {self.collection_name} not Exists, Creating..")
            return
        else:
            logger.info(f"Collection with name {self.collection_name} Already Exists.")
            print(f"Collection with name {self.collection_name} Already Exists.")
            return

    def store_items(self, doc_id, texts: list[str], metadatas: list[dict]):
        text_embeddings = embeddings.embed_documents(texts)
        points = []
        for embedding, text, metadata in zip(text_embeddings, texts, metadatas):
            point = {
                "id": doc_id,
                "vector": {
                    "dense_vector": embedding
                },
                "payload": {
                    "page_content": text,
                    "metadata": metadata
                }
            }
            points.append(point)

        response = requests.put(
            url= self.qdrant_url + f'/collections/{self.collection_name}/points?wait=true',
            json={"points": points},
            headers=self.headers
        )
        print(response.json())
        print("Added the data into Qdrant Database")        

    def delete_item(self, doc_id):
        r = requests.post(
            url=self.qdrant_url + f"/collections/{self.collection_name}/points/delete",
            headers=self.headers,
            json={
                "points": [doc_id]
            }
        )
        res = r.json()
        logger.info(f"Expense with {doc_id} deleted successfully.")
        print(f"Expense with {doc_id} deleted successfully. status {res.get('status')}")

    def check_or_create_index(self, index_name, schema: PayloadSchemaType):
        url = self.qdrant_url + f"/collections/{self.collection_name}"
        r = requests.get(
            url=url,
            headers=self.headers
        )
        response = r.json()
        result = response.get('result', {}).get('payload_schema')
        
        if index_name not in result:
            r = requests.put(
                url=url+'/index',
                headers=self.headers,
                json={
                    "field_name": index_name,
                    "field_schema": schema
                }
            )
            response = r.json()
            result = response.get('result')
            print(f"Index created for index name = {index_name} result = {result.get('status')}")
        else:
            print(f"Index already exists for '{index_name}'")
            
    def search_points(self, query, user_id, **kwargs):
        r = requests.post(
            url=self.qdrant_url + f"/collections/{self.collection_name}/points/query",
            headers=self.headers,
            json={
                "query": embeddings.embed_query(query),
                "limit": 20,
                "using": "dense_vector",
                "with_payload": True,
                "with_vectors": False,
                "filter.must.key": "metadata.user_id",
                "filter.must.match.value": str(user_id),
                "params.exact": True
            }
        )
        respose = r.json()
        search_results = respose.get('result').get('points')
        
        results = []
        for result in search_results:
            page_content = result.get('payload', {}).get('page_content')
            metadata = result.get('payload', {}).get('metadata') or {}
            metadata["_id"] = result.get('id')
            metadata["_collection_name"] = self.collection_name
            metadata["score"] = result.get('score')
            data = Document(page_content=page_content)
            # data = Document(page_content=page_content, metadata=metadata)
            results.append(data)
        
        print(f"found chunk : {len(results)} from Qdrant Database.")
        return results
    

