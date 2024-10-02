from django.urls import path
from . import views

urlpatterns = [
    path('api/genaitool/get_ai_response/', views.get_ai_response, name='get_ai_response'),
]