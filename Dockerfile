ARG VERSION=latest

FROM ubuntu:${VERSION}

Run apt-get update -y

CMD ["bash"] 