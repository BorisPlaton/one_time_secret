FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /one_time_secret

COPY . .
RUN pip install --no-cache-dir -r requirements/prod.txt && \
    rm -rf requirements