from django.urls import path
from .views import dino_start, dino_inference, inference_result

urlpatterns = [
    path('', dino_start, name='dino_start'),
    path('inference/', dino_inference, name='dino_inference'),
    path('inference_result/', inference_result, name='inference_result')
]