FROM python:3.10-slim

WORKDIR /.

COPY requirements.txt .

RUN python -m pip install --progress-bar off --upgrade pip
RUN python -m pip install --progress-bar off -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]