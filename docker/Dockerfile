FROM python:latest

RUN pip install rsa easyocr log4python fire

ADD ../ /root/TradingBot/

WORKDIR /root/TradingBot/

ENTRYPOINT python src/main.py daemon