from django.urls import path
from .views import classify_question, generate_agent_response

urlpatterns = [
    path('classify/', classify_question, name='classify_question'),
    path('generate-response/', generate_agent_response, name='generate_agent_response'),
]