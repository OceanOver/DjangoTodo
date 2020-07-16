
FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# update pip
RUN pip install pip -U
# install requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# copy code to container
COPY . /app

COPY ./docker/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

RUN cd /app/init.d && python initdb.py

EXPOSE 7009
