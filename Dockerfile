FROM python:3.9

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools \
    python3-wheel

COPY . /code
RUN pip install /code

CMD ["python", "-m", "sucinto"]