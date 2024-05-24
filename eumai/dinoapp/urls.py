from django.urls import path
from .views.dino import inference_start, inference_processing, inference_result

urlpatterns = [
    path('', inference_start, name='inference_start'),
    path('inference/', inference_processing, name='inference_processing'),
    path('inference_result/', inference_result, name='inference_result')
]