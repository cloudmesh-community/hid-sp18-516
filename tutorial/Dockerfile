FROM ubuntu:16.04
MAINTAINER Shagufta Pathan <spathan@iu.edu>

RUN apt-get update -q && apt-get install -qy \
 build-essential \
    python-dev \
    python-pip \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    pandoc \
    wget \
    curl \
    emacs \
    git-core \
    default-jre \
software-properties-common -y

# install net tools
RUN apt-get install -q -y net-tools

RUN git clone git://github.com/yyuu/pyenv.git .pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

ENV HOME  /
ENV PYENV_ROOT /.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 2.7.14
RUN pyenv global 2.7.14
RUN python -m ensurepip

RUN git clone -b master https://github.com/cloudmesh-community/hid-sp18-516.git

WORKDIR /hid-sp18-516/tutorial

CMD ["source", "cc-openrc.sh"]
#COPY cc-openrc.sh /hid-sp18-516/tutorial/

# install openstack cli and nova for python
RUN pip install python-openstackclient
RUN pip install python-novaclient

EXPOSE 8080
