FROM python:3.9-alpine

WORKDIR .

RUN apk add --no-cache gcc g++ musl-dev linux-headers postgresql-dev geos
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5005
CMD ["python", "main.py"]