FROM python:3.10-slim
RUN pip install requests
COPY . /app
CMD ["python", "/app/zabbix_add_ip.py"]
