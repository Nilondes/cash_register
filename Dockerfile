FROM python:3.12-slim

WORKDIR cash_register/

COPY requirements.txt /cash_register/

RUN pip install -r requirements.txt

COPY . /cash_register/

RUN ["chmod", "+x", "./docker-entrypoint.sh"]
ENTRYPOINT ["bash", "-c"]
CMD ["./docker-entrypoint.sh"]