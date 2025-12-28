from langchain_groq import ChatGroq
from django.conf import settings

llm = None
if settings.AI_ENABLED:
    llm = ChatGroq(
        model=settings.GROQ_LLM_MODEL,
        cache=False,
        verbose=True,
        api_key=settings.GROQ_API_KEY,
        streaming=False,
    )
