FROM python:3.12.5

WORKDIR /BOT

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

RUN pip install -U aiogram

COPY . .

CMD ["python", "run.py"]