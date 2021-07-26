#!/bin/sh
mkdir -p /var/log/heapdump
export JAVA_OPTS='-Xms512M -Xmx512M -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/log/ -XX:OnOutOfMemoryError="python3 /root/heapdump_handler.py"'
/usr/local/tomcat/bin/catalina.sh run

