FROM python:3.12
WORKDIR /api
COPY . /api

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt.txt

EXPOSE 8888

CMD ["python", "main.py"]

