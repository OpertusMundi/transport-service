FROM alpine:3.12 as build-stage-1

RUN apk update && \
  apk add --no-cache gcc g++ musl-dev python3 python3-dev py3-pip py3-setuptools py3-psutil

RUN ln -s $(which python3) /usr/bin/python

RUN pip3 install --upgrade pip && \
  pip3 install wheel && \
  pip3 install --prefix=/usr/local "tzlocal==3.0"

FROM alpine:3.12
ARG VERSION

RUN apk update && \
  apk add --no-cache git python3 python3-dev py3-pip py3-setuptools py3-psutil

LABEL language="python"
LABEL framework="flask"
LABEL usage="transport related requests on OSM network"

ENV VERSION="${VERSION}"
ENV PYTHON_VERSION="3.8"
ENV PYTHONPATH="/usr/local/lib/python${PYTHON_VERSION}/site-packages"

RUN addgroup flask && adduser -h /var/local/transport_service -D -G flask flask

COPY --from=build-stage-1 /usr/local/ /usr/local/

RUN mkdir /usr/local/transport_service/
COPY setup.py requirements.txt requirements-production.txt /usr/local/transport_service/

RUN pip3 install --upgrade pip && \
  pip3 install wheel && \
  (cd /usr/local/transport_service && pip3 install --no-cache-dir --prefix=/usr/local -r requirements.txt -r requirements-production.txt)
COPY transport_service /usr/local/transport_service/transport_service
RUN cd /usr/local/transport_service && python3 setup.py install --prefix=/usr/local && python3 setup.py clean -a

RUN ln -s $(which python3) /usr/bin/python

COPY wsgi.py docker-command.sh /usr/local/bin/
RUN chmod a+x /usr/local/bin/wsgi.py /usr/local/bin/docker-command.sh

WORKDIR /var/local/transport_service
RUN mkdir ./logs && chown flask:flask ./logs
COPY --chown=flask logging.conf .

ENV FLASK_APP="transport_service" \
    FLASK_ENV="production" \
    FLASK_DEBUG="false" \
    TLS_CERTIFICATE="" \
    TLS_KEY=""

USER flask
CMD ["/usr/local/bin/docker-command.sh"]

EXPOSE 5000
EXPOSE 5443
