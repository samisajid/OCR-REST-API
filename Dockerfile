FROM ubuntu:latest
MAINTAINER fnndsc "dev@babymri.org"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev tesseract-ocr libtesseract-dev libleptonica-dev pkg-config \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
RUN pip3 install flask
RUN pip3 install tesserocr 
RUN pip3 install Pillow
RUN pip3 install pybase64

COPY . /opt/

EXPOSE 5000

WORKDIR /opt

ENTRYPOINT ["python3"]
CMD ["server.py"]
