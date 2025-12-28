from django.conf import settings


def global_settings(request):
    return {
        "AI_ENABLED": settings.AI_ENABLED
    }