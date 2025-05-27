FROM ubuntu:latest
LABEL authors="nelson"

ENTRYPOINT ["top", "-b"]