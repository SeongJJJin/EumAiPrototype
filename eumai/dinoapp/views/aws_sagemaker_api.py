from dotenv import load_dotenv
import aioboto3
import os
import json

load_dotenv()


async def request_to_sagemaker(data):
    extracted_images = data

    sagemaker_session = aioboto3.Session(profile_name=os.getenv('PROFILE_NAME'),
                                         region_name=os.getenv('REGION_NAME'))

    async with sagemaker_session.client('sagemaker-runtime') as sagemaker_client:
        response = await sagemaker_client.invoke_endpoint(
            EndpointName=os.getenv('ENDPOINT_NAME'),
            ContentType='application/json',
            Body=json.dumps(extracted_images)
        )

        result = await response['Body'].read()
        result = json.loads(result)

        return result
