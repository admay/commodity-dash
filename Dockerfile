FROM python:3


COPY makefile /
COPY requirements.txt /

RUN make install

COPY data.csv /
COPY *.py /

EXPOSE 8080
CMD [ "make", "run-prod" ]
