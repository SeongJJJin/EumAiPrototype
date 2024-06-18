import json

from django.conf import settings
import requests
import os


class Inspection_api():
    def __init__(self, token, status, apt_pk):
        self.CHAEDLE_TOKEN = token
        self.STATUS = status
        self.APT_PK = apt_pk

    def inspection_list_request(self):
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Authorization': f'Bearer {self.CHAEDLE_TOKEN}',
            'Content-Type': 'application/json'
        }

        switch = True
        page_num = 1
        check_num = 1

        processed_data = {
            "total_list": 0,
            "defect_list": {}
        }

        try:
            while switch:
                if self.STATUS == 'ALL':
                    url = f'https://supervisor.api.chaedle.com/v1/defect/{self.APT_PK}?searchDateType=createdAt&searchType=RNL%2BCL%2BRL&page={page_num}&limit=15'
                else:
                    url = f'https://supervisor.api.chaedle.com/v1/defect/{self.APT_PK}?status={self.STATUS}&searchDateType=createdAt&searchType=RNL%2BCL%2BRL&page={page_num}&limit=15'

                response = requests.get(url, headers=headers)
                processing_data = response.json()["items"]
                processed_data["total_list"] = response.json()["pagination"]["totalRecord"]

                for i in range(len(processing_data)):
                    processed_data["defect_list"][check_num] = {
                        "apartmentIdx": processing_data[i]["apartmentIdx"],
                        "dong": processing_data[i]["dong"],
                        "ho": processing_data[i]["ho"],
                        "location": processing_data[i]["location"],
                        "content": processing_data[i]["content"],
                        "construct_type": {},
                        "detail_construct_type": {},
                        "defect": {},
                        "images": [processing_data[i]["upload"][j]["url"] for j in range(len(processing_data[i]["upload"]))],
                        "status": processing_data[i]["status"]
                    }

                    check_num += 1

                if page_num > response.json()["pagination"]["totalPage"]:
                    switch = False
                else:
                    page_num += 1

                print(page_num)

            return processed_data
        except KeyError:
            raise


class Defect_mapping_data_api():

    def __init__(self, token):
        self.CHAEDLE_TOKEN = token

    def defect_mapping_data(self):
        try:
            # 실제 API 요청 로직

            # 로컬 테스트
            mapping_data_path = os.path.join(settings.DINOAPP_STATIC_ROOT, "jsons/ai.json")
            with open(mapping_data_path, "r", encoding='utf-8') as f:
                data = json.load(f)

            return data
        except Exception as e:
            return e


