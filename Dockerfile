FROM base_image:latest

# RUN apt-get update && apt-get install git -y
# RUN mkdir /fazumbem
# RUN git clone https://2b7a27bca6b78e559fd1c5e4f42b6b8de9112c26@github.com/fazumbem/fazumbem
COPY . /fazumbem/api
WORKDIR /fazumbem/api
ENTRYPOINT ["python"]
CMD ["webapp.py"]


