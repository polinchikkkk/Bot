FROM python:3.12.5 
 
COPY requirements.txt /code/requirements.txt  
 
RUN pip install --no-cache-dir -r /code/requirements.txt 
 
COPY . /bot/ 
 
CMD ["python", "/bot/run.py"]
