FROM       centos:7
MAINTAINER sqre-admin
LABEL      description="LSST DM/SQuaRE status microservice" \
           name="lsstsqre/uservice-status"

USER       root
RUN        yum update -y
RUN        yum install -y epel-release
RUN        yum repolist
RUN        yum install -y git python-pip python-devel
RUN        yum install -y gcc openssl-devel
RUN        pip install --upgrade pip
RUN        useradd -d /home/uwsgi -m uwsgi
RUN        mkdir /dist

ARG        VERSION="0.1.0"
LABEL      version="$VERSION"
COPY       dist/sqre-uservice-status-$VERSION.tar.gz /dist
RUN        pip install /dist/sqre-uservice-status-$VERSION.tar.gz

USER uwsgi
WORKDIR /home/uwsgi
COPY uwsgi.ini .
EXPOSE 5000
CMD [ "uwsgi", "-T", "uwsgi.ini" ]

