FROM python:3.7.13-slim-bullseye

WORKDIR /usr/app

EXPOSE 8000

RUN apt-get update -y

RUN python -m pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:server", "--timeout", "90", "--log-level", "DEBUG", "--log-file", "-"]