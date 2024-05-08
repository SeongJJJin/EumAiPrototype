FROM python:3.9-alpine
RUN apk add gcc musl-dev

COPY . /app
WORKDIR /app
RUN python -m venv venv && . venv/bin/activate
RUN pip3 install -r requirements.txt

ENV PROFILE_NAME eum
ENV REGION_NAME ap-northeast-2
ENV ENDPOINT_NAME dinov2-20240508125943

WORKDIR /app/eumai
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000