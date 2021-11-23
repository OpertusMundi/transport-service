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

ENV VERSION="${VERSION}"
ENV PYTHON_VERSION="3.8"
ENV PYTHONPATH="/usr/local/lib/python${PYTHON_VERSION}/site-packages"

COPY --from=build-stage-1 /usr/local/ /usr/local/

COPY setup.py requirements.txt requirements-testing.txt ./
RUN pip3 install --upgrade pip && \
  pip3 install wheel && \
  pip3 install --no-cache-dir --prefix=/usr/local -r requirements.txt -r requirements-testing.txt

ENV FLASK_APP="transport_service" \
    FLASK_ENV="testing" \
    FLASK_DEBUG="false"

COPY run-nosetests.sh /
RUN chmod a+x /run-nosetests.sh
ENTRYPOINT ["/run-nosetests.sh"]
