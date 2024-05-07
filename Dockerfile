FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .
ARG token
ENV KPO_TOKEN $token
CMD python3 main.py
