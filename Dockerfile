# start by pulling the python image
FROM python:3.10.2-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

#RUN apk update && apk add tzdata

# install the dependencies and packages in the requirements file
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy every content from the local file to the image
COPY src /app
COPY entry.sh /entry.sh

EXPOSE 5000

#RUN echo '*       *       *       *       *       run-parts /entry.sh > /entry.log' >> /etc/crontabs/root

# configure the container to run in an executed manner
ENTRYPOINT [ "sh" ]

CMD ["/entry.sh" ]

