FROM python:3.12
WORKDIR /analysis_service
COPY . /analysis_service

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt.txt

EXPOSE 8887

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8887"]
