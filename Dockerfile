FROM python:3.8

WORKDIR /salary_data_ggregation

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
