FROM python:3.10

# environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ENV=prod


WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 8080

# run the application
ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8080 --workers 2
