FROM python:3.10

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5004

CMD ["python", "run.py"]