FROM python:latest

RUN pip install rsa pyyaml

ADD ../ /root/TradingBot/

WORKDIR /root/TradingBot/

ENTRYPOINT python src/main.py daemon