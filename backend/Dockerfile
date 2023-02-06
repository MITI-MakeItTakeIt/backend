FROM python:3.9
ENV PYTHONUNBUFFERED=1

WORKDIR /backend

COPY . /backend/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh