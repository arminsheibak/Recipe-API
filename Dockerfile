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
RUN pip install -r requirement.txt

# Copy project
COPY . .

RUN adduser -D user
USER user

