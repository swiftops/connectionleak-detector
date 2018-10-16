FROM python:alpine

RUN mkdir -p /app/work/salm_core

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5004

CMD [ "gunicorn", "--config", "gunicorn_config.py", "services:app" ]
