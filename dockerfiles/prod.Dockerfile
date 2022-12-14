FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY ../requirements.prod.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.prod.txt
COPY .. /code/

COPY ../entrypoint.prod.sh /
ENTRYPOINT ["sh", "./entrypoint.prod.sh"]