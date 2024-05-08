### 실행
```
docker run --name {container_name} -v ~/.aws:/root/.aws -e PROFILE_NAME={profile_name} -e ENDPOINT_NAME={endopoint_name} -p 8000:8000 {image_name}
```
