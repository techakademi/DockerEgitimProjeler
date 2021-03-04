FROM python:3.6

ENV WEB_UYGULAMA=/usr/src/app

WORKDIR ${WEB_UYGULAMA}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN pip install --upgrade pip
COPY ./requirements.txt ${WEB_UYGULAMA}/requirements.txt
RUN pip install -r requirements.txt

COPY .  /${WEB_UYGULAMA}

CMD [ "gunicorn", "--log-level=debug", "-b 0.0.0.0:5000", "manage:app" ]

RUN chmod +x /usr/src/app/crmimhaet.sh

ENTRYPOINT [ "/usr/src/app/crmimhaet.sh" ]