FROM python:3.8

WORKDIR /home/www/
COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt
RUN chmod o+x entrypoint.sh
RUN ls
COPY . .
RUN ls
ENTRYPOINT ["/home/www/entrypoint.sh"]