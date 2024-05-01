FROM public.ecr.aws/amazonlinux/amazonlinux:latest

# Install SQLite and Apache
RUN yum update -y && \
    yum install -y sqlite sqlite-devel httpd && \
    yum clean all

WORKDIR /data

COPY ./crsqlite.so /data/

ENV LD_LIBRARY_PATH=/data:${LD_LIBRARY_PATH}

# Configure Apache to run in the foreground
RUN echo '#!/bin/bash' > /root/run_apache.sh && \
    echo 'mkdir -p /var/run/httpd' >> /root/run_apache.sh && \
    echo 'mkdir -p /var/lock/httpd' >> /root/run_apache.sh && \
    echo 'exec /usr/sbin/httpd -D FOREGROUND' >> /root/run_apache.sh && \
    chmod +x /root/run_apache.sh


CMD ["/root/run_apache.sh"]
