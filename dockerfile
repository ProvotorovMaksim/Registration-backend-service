FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY entry.sh /entry.sh

RUN chmod +x /entry.sh

EXPOSE 8001

ENTRYPOINT ["/entry.sh"]