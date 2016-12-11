FROM jbonachera/arch
MAINTAINER Julien BONACHERA <julien@bonachera.fr>
ENTRYPOINT /sbin/entrypoint.sh
EXPOSE 24 143 993 4190
VOLUME ["/srv/vmail", "/etc/dovecot/auth"]
RUN pacman -S --noconfirm dovecot pigeonhole && \
    mv /etc/dovecot/dovecot.conf.sample /etc/dovecot/dovecot.conf
RUN groupadd -g 5000 vmail
RUN useradd -r vmail -u 5000 -g 5000
COPY conf.d/* /etc/dovecot/conf.d/
COPY templates /etc/dovecot/templates/
COPY scripts/* /usr/local/bin/
ADD entrypoint.sh /sbin/entrypoint.sh

