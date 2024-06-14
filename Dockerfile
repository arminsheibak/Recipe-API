# Pull base image 
FROM python:3.12-alpine

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir app
WORKDIR /app

# Install dependencies
COPY ./requirement.txt ./
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers postgresql-dev
RUN pip install -r requirement.txt
RUN apk del .tmp-build-deps

# Copy project
COPY . .

RUN adduser -D user
USER user

