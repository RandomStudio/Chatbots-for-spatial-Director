from django.urls import path
from .views import chat_completion


urlpatterns = [
    path("chatCompletion", chat_completion),
]
