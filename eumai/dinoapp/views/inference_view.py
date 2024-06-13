import asyncio
from asgiref.sync import async_to_sync
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .supervisor_api import Inspection_api
from .data_process import extract_image, insert_construct_all_defect, split_dict
from .aws_sagemaker_api import request_to_sagemaker
import os
import json

load_dotenv()
token = os.getenv('TOKEN')
apt_pk = os.getenv('DEFAULT_APT_PK')
status = os.getenv('DEFAULT_STATUS')

inspection_data = {}
error_results_dic = {}

def apart_detail_selecter(request):
    return render(request, 'dinoapp/apart_detail_selecter.html')

@csrf_exempt
def inference_start(request):
    global inspection_data

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            apt_pk = json.loads(os.getenv('APT_PK'))[data.get('apt_name')]
            status = json.loads(os.getenv("STATUS"))[data.get('status_name')]

            try:
                inspection_data = Inspection_api(token, status, apt_pk).inspection_list_request()
            except KeyError:
                print("inspection_data 함수 문제")

        except KeyError:
            print("apt_pk or status 존재 하지 않음.")
            inspection_data = {}

    return render(request, 'dinoapp/dino_start.html', {'inspection_data': inspection_data})


@async_to_sync
async def inference_processing(request):
    if request.method == 'POST':
        all_result = await async_inference_processing()

        global error_results_dic
        error_results_dic = all_result

        return JsonResponse(error_results_dic)
    else:
        return render(request, 'dinoapp/dino_start.html')

async def async_inference_processing():
    all_result = {}

    extracted_images = extract_image(inspection_data)
    chunks = split_dict(extracted_images, 2)
    tasks = [request_to_sagemaker(chunk) for chunk in chunks]

    batch_size = 150

    for i in range(0, len(tasks), batch_size):
        batch_task = tasks[i:i+batch_size]
        results = await asyncio.gather(*batch_task)

        for result in results:
            all_result.update(result)

    return all_result

def inference_result(request):
    print(error_results_dic)
    final_data = insert_construct_all_defect(inspection_data, error_results_dic)
    return render(request, 'dinoapp/dino_result.html', {"final_data": final_data})





# 데이터 수정 및 적용 했을 때 처리 함수
def update_data(request):
    if request == 'POST':

        data = json.loads(request.body())
        return JsonResponse(data)
    else:
        return JsonResponse("잘못된 요청~~")