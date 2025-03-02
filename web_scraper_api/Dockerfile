FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

RUN adduser -D -h /home/nonrootuser -s /bin/bash nonrootuser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R nonrootuser:nonrootuser /app
USER nonrootuser

ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
