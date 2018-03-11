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

RUN git clone git://github.com/yyuu/pyenv.git .pyenv
RUN git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

ENV HOME  /
ENV PYENV_ROOT /.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH

RUN pyenv install 2.7.14
RUN pyenv global 2.7.14
RUN python -m ensurepip

RUN git clone https://github.com/cloudmesh-community/hid-sp18-516.git

WORKDIR /hid-sp18-516/swagger

RUN wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar -O swagger-codegen-cli.jar
#RUN java -jar swagger-codegen-cli.jar generate -i localhost.yaml -l python-flask -o server -D supportPython2=true
#RUN cp *.py server/swagger_server/controllers
#RUN cp security.yaml ~/.cloudmesh/
#RUN cd server && pip install -r requirements.txt && python setup.py install

EXPOSE 8080

#CMD cd /hid-sp18-516/swagger/server && pip install -r requirements.txt
RUN make service

#RUN make start
#ENTRYPOINT["make"]
CMD ["make start"]

