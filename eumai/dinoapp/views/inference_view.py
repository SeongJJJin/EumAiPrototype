import asyncio
from asgiref.sync import async_to_sync
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .supervisor_api import Inspection_api, Defect_mapping_data_api
from .data_process import extract_image, insert_construct_all_defect, split_dict, insert_modified_data
from .aws_sagemaker_api import request_to_sagemaker
import os
import json

load_dotenv()
token = os.getenv('TOKEN')
apt_pk = os.getenv('DEFAULT_APT_PK')
status = os.getenv('DEFAULT_STATUS')

inspection_data = {}
error_results = {}
final_data = {}
modified_final_data = {}
defect_mapping_data = Defect_mapping_data_api(token).defect_mapping_data()

def apart_detail_selecter(request):
    return render(request, 'apart_selecter_view.html')

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

    return render(request, 'inference_start_view.html', {'inspection_data': inspection_data})


@async_to_sync
async def inference_processing(request):
    if request.method == "POST":
        all_result = await async_inference_processing()

        global error_results
        error_results = all_result

        return JsonResponse(error_results)
    else:
        return render(request, 'inference_start_view.html')

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
    global final_data
    # 추론 결과 데이터
    final_data = insert_construct_all_defect(inspection_data, error_results)

    # 아파트 별 맵핑 데이터
    return render(request, 'inference_result_view.html', {"final_data": final_data, "defect_mapping_data": defect_mapping_data})


def update_data(request):
    global modified_final_data

    if request.method == "POST":
        modified_error_results = json.loads(request.body)

        if not modified_error_results:
            modified_final_data = final_data
        else:
            modified_final_data = insert_modified_data(inspection_data, modified_error_results)

    return render(request, 'modified_defect_list_view.html', {"modified_final_data": modified_final_data})





