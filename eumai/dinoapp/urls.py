from django.urls import path
from dinoapp.views.inference_view import inference_start, inference_processing, inference_result, update_data, apart_detail_selecter

urlpatterns = [
    path('', apart_detail_selecter, name='apart_detail_selecter'),
    path('inference_start/', inference_start, name='inference_start'),
    path('inference_processing/', inference_processing, name='inference_processing'),
    path('inference_result/', inference_result, name='inference_result'),
    path('update_data/', update_data, name='update_data')
]