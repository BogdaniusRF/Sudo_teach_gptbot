FROM python

WORKDIR /app

COPY requirements.txt .

RUN pip install --nocache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]