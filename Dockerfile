FROM python:3.8
COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]