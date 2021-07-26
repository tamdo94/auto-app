FROM tomcat:jdk11-openjdk-slim

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-setuptools \
        groff \
        less \
    && pip3 install --upgrade pip \
    && apt-get clean

RUN pip install boto3

RUN pip3 --no-cache-dir install --upgrade awscli

RUN apt-get install -y vim

COPY web-app/target/web-app.war /usr/local/tomcat/webapps/ROOT.war
COPY entrypoint.sh /entrypoint.sh
COPY heapdump_handler.py /root/heapdump_handler.py

ENTRYPOINT [ "bash", "/entrypoint.sh" ]