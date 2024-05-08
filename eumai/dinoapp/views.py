import os
from dotenv import load_dotenv
from django.shortcuts import render
from django.http import JsonResponse
from glob import glob
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import boto3


load_dotenv()
TILE = ["TILE_BREAK", "TILE_CRACK", "TILE_ERROR_LINE", "TILE_SCRATCH"]
PAPER = ["PAPERING_BREAK", "PAPERING_ERROR_COTTON", "PAPERING_ERROR_JOINT", "PAPERING_EXCITED_HOLD", "PAPERING_MOLD", "PAPERING_POLLUTION_HOLD", "PAPERING_UNDEVELOPED", "PAPERING_WRINKLE_HOLD"]
error_results_dic = {}
def inference_result(request):
    items = error_results_dic.items()
    context = {'error_results_dic': items}
    return render(request, 'dinoapp/dino_result.html', context)

def dino_start(request):
    return render(request, 'dinoapp/dino_start.html')

@csrf_exempt
def dino_inference(request):
    if request.method == 'POST':
        bytes_dic = image_to_text()
        result_dic = {}
        for key, value in bytes_dic.items():

            sagemaker_session = boto3.Session(profile_name=os.getenv('PROFILE_NAME'),
                                              region_name=os.getenv('REGION_NAME'))
            sagemaker_client = sagemaker_session.client('sagemaker-runtime')
            response = sagemaker_client.invoke_endpoint(
                EndpointName=os.getenv('ENDPOINT_NAME'),
                ContentType='application/text',
                Body=value
            )

            result = response['Body'].read()
            result = result.decode('utf-8')
            result_dic[key] = json.loads(result)

        error_results_dic = result_process(result_dic)
        return JsonResponse(error_results_dic)
    else:
        return render(request, 'dinoapp/dino_start.html')

def result_process(result_dic):
    # 0 : null, 1 : Tile, 2 : Paper
    for file_path in result_dic.keys():
        file_name = file_name_slicer(file_path)

        if result_dic[file_path]["prediction"][1][0] == 0: # null
            print("NULL")
            error_results_dic[file_name] = ["NULL", "NULL", "NULL"]

        elif result_dic[file_path]["prediction"][1][0] == 1: # Tile
            tile_error_num = find_index(result_dic[file_path]["prediction"][2][0])
            print("TILE", TILE[tile_error_num])
            error_results_dic[file_name] = ["NULL", "TILE", TILE[tile_error_num]]

        elif result_dic[file_path]["prediction"][1][0] == 2: # Paper
            paper_error_num = find_index(result_dic[file_path]["prediction"][2][0])
            print("PAPER", PAPER[paper_error_num])
            error_results_dic[file_name] = ["NULL", "PAPER", PAPER[paper_error_num]]

        else:
            pass

    return error_results_dic

def file_name_slicer(file_path):
    file_name = os.path.basename(file_path)
    return file_name

def find_index(acc_list):
    max_value = max(acc_list)
    return acc_list.index(max_value)


def image_to_text():
    path = os.path.join(settings.DINOAPP_STATIC_ROOT, 'images/*')
    img_list = glob(path)
    bytes_dic = {}
    for image in img_list:
        with open(image, 'rb') as img:
            bytes_img = bytearray(img.read())
            bytes_dic[image] = bytes_img

    return bytes_dic