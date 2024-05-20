FROM python:3.10-alpine
WORKDIR /bot
RUN apk update
RUN apk add --no-cache gcc musl-dev linux-headers python3-dev libpq-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "./bot.py"]
