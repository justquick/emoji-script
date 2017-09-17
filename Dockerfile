FROM python:alpine

RUN pip install tox

CMD ["python"]
