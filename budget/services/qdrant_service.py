from qdrant_client import QdrantClient, models
from qdrant_client.models import PayloadSchemaType
from langchain_core.documents import Document
from django.conf import settings
import logging as logger


if settings.AI_ENABLED:
    from budget.services.embeddings import embeddings


class QdrantService:
    qdrant_api_key = settings.QDRANT_API_KEY
    qdrant_url = settings.QDRANT_URL
    collection_name = settings.QDRANT_COLLECTION
    qdrant_client = None

    def __init__(self, **kwargs):    
        if settings.AI_ENABLED:
            self.qdrant_client: QdrantClient = self.get_qdrant_client(**kwargs)
            self.check_or_create_collection()               
            self.check_or_create_index('id', PayloadSchemaType.INTEGER)
            self.check_or_create_index('user_id', PayloadSchemaType.UUID)

    def get_qdrant_client(self, **kwargs):
        return QdrantClient(api_key=self.qdrant_api_key, url=self.qdrant_url, **kwargs)

    def check_or_create_collection(self):
        if not self.qdrant_client.collection_exists(self.collection_name):
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config={
                    "dense_vector": models.VectorParams(
                        size=embeddings.get_embeddings_dimension(),
                        distance=models.Distance.COSINE,
                    )
                },
            )
            logger.info(f"Collection with name {self.collection_name} not Exists, Creating..")
            return

        logger.info(f"Collection with name {self.collection_name} Already Exists.")

    def store_items(self, doc_id, texts, metadatas):
        text_embeddings = embeddings.embed_documents(texts)
        points = []
        for embedding, text, metadata in zip(text_embeddings, texts, metadatas):
            point = models.PointStruct(
                id=doc_id,
                vector={
                    "dense_vector": embedding,
                },
                payload={
                    "page_content": text,
                    "metadata": metadata
                }
            )
            points.append(point)
            
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def delete_item(self, doc_id):
        self.qdrant_client.delete(
            collection_name=self.collection_name,
            points_selector=[doc_id]
        )
        logger.info(f"Expense with {doc_id} deleted successfully.")

    def check_or_create_index(self, index_name, schema: PayloadSchemaType):
        info = self.qdrant_client.get_collection(self.collection_name)
        if index_name not in info.payload_schema:
            self.qdrant_client.create_payload_index(
                collection_name=self.collection_name,
                field_name=index_name,
                field_schema=schema
            )
            print(f"Index created for '{index_name}'")
        else:
            print(f"Index already exists for '{index_name}'")
            
    def search_points(self, query, user_id, **kwargs):
        search_results = self.qdrant_client.query_points(
            collection_name=self.collection_name,
            query=embeddings.embed_query(query),
            limit=20,
            with_payload=True,
            with_vectors=False,
            query_filter=models.Filter(
                must=models.FieldCondition(
                    key="metadata.user_id",
                    match=models.MatchValue(
                        value=str(user_id)
                    )
                )
            ),
            search_params=models.SearchParams(exact=True),
            using="dense_vector",
            **kwargs
        ).points
        
        results = []
        for result in search_results:
            page_content = result.payload.get('page_content')
            metadata = result.payload.get('metadata') or {}
            metadata["_id"] = result.id
            metadata["_collection_name"] = self.collection_name
            metadata["score"] = result.score
            data = Document(page_content=page_content)
            # data = Document(page_content=page_content, metadata=metadata)
            results.append(data)
        
        return results
    

qdrant_db = QdrantService()
