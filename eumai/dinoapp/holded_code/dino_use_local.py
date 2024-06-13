# from dotenv import load_dotenv
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.conf import settings
# from django.views.decorators.csrf import csrf_exempt
# from ..fixedValue.errors_category import MAINTYPE, SUBTYPE, ERRORS
# import os
# import json
# import boto3
#
# load_dotenv()
#
#
# def inference_start(request):
#     images_dir = os.path.join(settings.DINOAPP_STATIC_ROOT, 'images')
#     image_files = [os.path.join('images', img) for img in os.listdir(images_dir) if img.endswith((".png", ".jpg"))]
#     context = {"image_files" : image_files}
#     return render(request, 'dinoapp/dino_start.html', context)
#
# @csrf_exempt
# def inference_processing(request):
#     if request.method == 'POST':
#
#         selected_image = json.loads(request.body.decode('utf-8'))
#         selected_image_list = selected_image.get('images', [])
#         bytes_dic = image_to_text(selected_image_list)
#
#         result_dic = {}
#         for key, value in bytes_dic.items():
#
#             sagemaker_session = boto3.Session(profile_name=os.getenv('PROFILE_NAME'),
#                                               region_name=os.getenv('REGION_NAME'))
#             sagemaker_client = sagemaker_session.client('sagemaker-runtime')
#             response = sagemaker_client.invoke_endpoint(
#                 EndpointName=os.getenv('ENDPOINT_NAME'),
#                 ContentType='application/text',
#                 Body=value # 이미지 url
#             )
#
#             result = response['Body'].read()
#             result = result.decode('utf-8')
#             result_dic[key] = json.loads(result)
#
#         global error_results_dic
#         error_results_dic = {}
#         error_results_dic = result_processing(result_dic)
#
#         return JsonResponse(error_results_dic)
#     else:
#         return render(request, 'dinoapp/dino_start.html')
#
# def inference_result(request):
#     items = error_results_dic.items()
#     context = {
#         'error_results_dic': items,
#         'main_type': MAINTYPE,
#         'sub_type': SUBTYPE,
#         'errors' : []
#     }
#     return render(request, 'dinoapp/dino_result.html', context)
#
# def result_processing(result_dic):
#     # 0 : null, 1 : Tile, 2 : Paper
#     for file_path in result_dic.keys():
#         file_name = file_name_slicer(file_path)
#
#         if result_dic[file_path]["prediction"][1][0] == 0: # null
#             print("NULL")
#             error_results_dic[file_name] = ["NULL", "NULL", "NULL"]
#
#         elif result_dic[file_path]["prediction"][1][0] == 1: # Tile
#             tile_errors = find_index(result_dic[file_path]["prediction"][2][0])
#             error_results_dic[file_name] = [MAINTYPE[0], SUBTYPE[0], [ERRORS[SUBTYPE[0]][i] for i in tile_errors]]
#
#         elif result_dic[file_path]["prediction"][1][0] == 2: # Paper
#             paper_errors = find_index(result_dic[file_path]["prediction"][2][0])
#             error_results_dic[file_name] = [MAINTYPE[0], SUBTYPE[1], [ERRORS[SUBTYPE[1]][i] for i in paper_errors]]
#
#         else:
#             pass
#
#     return error_results_dic
#
# def file_name_slicer(file_path):
#     file_name = os.path.basename(file_path)
#     return file_name
#
# def find_index(acc_list):
#     errors = []
#     for score in acc_list:
#         if score >= 0.3:
#             errors.append(acc_list.index(score))
#
#     if len(errors) == 0:
#         max_score = max(acc_list)
#         errors.append(acc_list.index(max_score))
#
#     return errors
#
# def image_to_text(selected_image_list):
#     bytes_dic = {}
#
#     for selected_image in selected_image_list:
#         selected_image_path = os.path.join(settings.DINOAPP_STATIC_ROOT, selected_image)
#         with open(selected_image_path, 'rb') as img:
#             bytes_img = bytearray(img.read())
#             bytes_dic[selected_image] = bytes_img
#
#     return bytes_dic