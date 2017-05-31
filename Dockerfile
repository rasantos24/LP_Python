FROM python:2.7.12

RUN git clone https://github.com/rasantos24/LP_Python

RUN pip install requests

EXPOSE 8080

CMD cd LP_Python && python tareaPython2.py
