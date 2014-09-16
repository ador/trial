FROM quay.io/ador/yo-base
MAINTAINER Adrienn Szabo "adrienn.szabo4@gmail.com"

RUN apt-get update && apt-get install -yq libcurl4-gnutls-dev libxml2-dev software-properties-common
RUN sudo add-apt-repository -y ppa:marutter/rrutter
RUN sudo apt-get update && apt-get install -yq r-base r-base-dev

ENV HOME /home/yoda
USER yoda
RUN mkdir -p /home/yoda/git && cd /home/yoda/git

