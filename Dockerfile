FROM       centos:7
MAINTAINER sqre-admin
LABEL      version="0.0.7" description="LSST DM/SQuaRE status microservice" \
           name="lsstsqre/uservice-status"

USER       root
RUN        yum update -y && \
           yum install -y epel-release && \
           yum repolist && \
           yum install -y git python-pip python-devel && \
	   pip install --upgrade pip && \
           pip install sqre-uservice-status && \
           useradd -d /home/flasker -m flasker

USER flasker
WORKDIR /home/flasker
EXPOSE 5000
CMD sqre-uservice-status
	   
