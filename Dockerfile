FROM python:3-alpine
#RUN yum groupinstall "Development Tools"
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 5001

ENTRYPOINT ["python"]

CMD ["flask_rest/app.py"]
