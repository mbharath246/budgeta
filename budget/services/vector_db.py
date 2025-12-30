from django.conf import settings


if settings.VECTOR_DB_NAME.lower() == "pinecone":
    from budget.services.pinecone_service import PineconeService
    vector_db = PineconeService()
    print("Connected to Qdrant Database")
    
elif settings.VECTOR_DB_NAME.lower() == "qdrant":
    from budget.services.qdrant_service import QdrantService
    vector_db = QdrantService()
    print("Connected to Pinecone Database") 
    
else:
    vector_db = None
    