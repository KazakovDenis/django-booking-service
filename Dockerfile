# cmd to build:
# docker build -t booking:1.0 --build-arg BOOKING_SECRET=$BOOKING_SECRET .
#
# cmd to run:
# docker run --name booking --rm -d -p 8000:8000 booking:1.0
FROM python:3.8-alpine
LABEL maintainer="https://github.com/KazakovDenis"

# environment preparations
WORKDIR /www
COPY requirements/base.txt ./requirements.txt
RUN python3 -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
ARG BOOKING_SECRET
ENV BOOKING_SECRET=$BOOKING_SECRET

# project preparations
COPY booking_service .
EXPOSE 8000
RUN python3 manage.py makemigrations && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput
CMD python3 manage.py runserver 0.0.0.0:8000
