FROM python:3.11-slim
WORKDIR /sim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY simulator.py .
CMD ["python", "simulator.py"]
