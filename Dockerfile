FROM python

ENV API_ID=
ENV API_HASH=
ENV BOT_TOKEN=
ENV WEATHER_API=

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]

