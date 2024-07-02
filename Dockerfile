FROM python:3.10-slim
RUN pip install requests
COPY . /app
CMD ["python", "/app/create_host.py"]
