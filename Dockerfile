FROM docker.io/jbonachera/consul-template
MAINTAINER Julien BONACHERA <julien@bonachera.fr>
ONBUILD COPY consul-template.d/* /etc/consul-template/
ONBUILD COPY conf.d/* /etc/dovecot/conf.d
RUN dnf install -y dovecot dovecot-pigeonhole dovecot-mysql
COPY reload_dovecot_if_running /usr/local/bin/reload_dovecot_if_running
RUN chmod +x /usr/local/bin/reload_*_if_running
VOLUME ["/srv/vmail"]
RUN groupadd -g 5000 vmail
RUN useradd -r vmail -u 5000 -g 5000
EXPOSE 24 143 993 4190
