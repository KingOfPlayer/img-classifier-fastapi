FROM python:3.12-bookworm
RUN apt-get update
RUN apt-get install libgl1 -y
RUN pip install --upgrade pip
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src ./src
WORKDIR /code/src
CMD ["python", "main.py"] 