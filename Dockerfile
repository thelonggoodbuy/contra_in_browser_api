# pull official base python image
FROM python:3.11.9

# set the work directory inside docker image
WORKDIR /usr/src/app

# sen enviroment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHOBUNBUFFERED 1

# install libraries
RUN apt update
RUN echo y|apt install postgresql  
RUN apt install postgresql-contrib
RUN apt install libpq-dev
RUN pip install psycopg2
# RUN echo y|apt install wkhtmltopdf
RUN apt install -y netcat-traditional
RUN apt install make
RUN echo y|apt install vim
RUN echo y|apt install libevent-dev


# install dependencies (!)
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt


COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
RUN echo '-----------1---------------------------------------'

COPY . /usr/src/app/

# (What is it?)
# EXPOSE 3000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]