from pinecone import Pinecone, ServerlessSpec, VectorType, Metric, CloudProvider, AwsRegion
from langchain_core.documents import Document
from django.conf import settings

if settings.AI_ENABLED:
    from budget.services.embeddings import embeddings


class PineconeService:
    
    def __init__(self):        
        self.index_name = settings.PINECONE_INDEX_NAME
        self.payload_text: str = "text"
        self.top_k = settings.PINECONE_TOP_K
        self.pinecone_client = self.get_pinecone_client()
        self.index = self.get_or_create_index(self.index_name)
    
    def get_pinecone_client(self):
        return Pinecone(api_key=settings.PINECONE_API_KEY)
    
    def get_or_create_index(self, index_name):
        if not self.pinecone_client.has_index(index_name):
            self.pinecone_client.create_index(
                name=index_name,
                vector_type=VectorType.DENSE,
                metric=Metric.COSINE,
                spec=ServerlessSpec(cloud=CloudProvider.AWS, region=AwsRegion.US_EAST_1),
                dimension=embeddings.get_embeddings_dimension()
            )
        self.index = self.pinecone_client.Index(index_name)
        return self.index         
    
    def store_items(self, doc_id, texts: list[str], metadatas: list[dict]):
        text_embeddings = embeddings.embed_documents(texts)
        documents = []
        for text, embedding, metadata in zip(texts, text_embeddings, metadatas):
            metadata[self.payload_text] = text
            vector_tuple = (str(doc_id), embedding, metadata)
            documents.append(vector_tuple)
            
        self.index.upsert(
            vectors=documents
        )
        print("Added the data into Pinecone Database")
        
    def delete_item(self, doc_id):
        self.index.delete([str(doc_id)])
        print(f"Deleted the data with id {doc_id} from Pinecone Database")
        
        
    def search_points(self, query, user_id):
        search_results = self.index.query(
            vector=embeddings.embed_query(query), 
            top_k=20,
            filter={
                "user_id": {"$eq": str(user_id)}
            },
            include_metadata=True,
            include_values=False
        )

        search_results = search_results.get('matches')
                
        results = []
        for result in search_results:
            metadata = result.get('metadata')
            page_content = metadata.pop('text')
            metadata["score"] = result.get('score')
            data = Document(page_content=page_content)
            # data = Document(page_content=page_content, metadata=metadata)
            results.append(data)
        
        print(f"found chunk : {len(results)} from Pinecone Database.")
        return results
    