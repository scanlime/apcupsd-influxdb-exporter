FROM jfloff/alpine-python

RUN apk add --no-cache apcupsd jq curl busybox supervisor
COPY ./conf/requirements.txt /requirements.txt
COPY ./conf/apcupsd.conf /
COPY ./src/app.py /
RUN pip install -r /requirements.txt
COPY ./conf/supervisord.conf /supervisord.conf

CMD ["supervisord", "-n", "-c","/supervisord.conf"]