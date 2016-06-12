FROM fedora
MAINTAINER Julien BONACHERA <julien@bonachera.fr>
ENTRYPOINT /sbin/entrypoint.sh
COPY conf.d/* /etc/dovecot/conf.d
RUN dnf install -y dovecot dovecot-pigeonhole dovecot-mysql
VOLUME ["/srv/vmail"]
RUN groupadd -g 5000 vmail
RUN useradd -r vmail -u 5000 -g 5000
EXPOSE 24 143 993 4190
ADD entrypoint.sh /sbin/entrypoint.sh

