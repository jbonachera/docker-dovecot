#!/bin/bash
trap 'exit' INT

render.py /etc/dovecot/templates/10-ssl.conf.jinja2 > /etc/dovecot/conf.d/10-ssl.conf
render.py /etc/dovecot/templates/10-master.conf.jinja2 > /etc/dovecot/conf.d/10-master.conf

#fix volume perms
chown vmail:vmail /srv/vmail
chmod 750 /srv/vmail

if [ -n "$SEED_USERS" ]; then
    for user_data in $SEED_USERS; do
        domain=$(echo $user_data | cut -f 1 -d : )
        user=$(echo $user_data | cut -f 2 -d : )
        password=$(echo $user_data | cut -f 3 -d :)
        /usr/local/bin/dove-adduser $domain $user $password
    done
fi

echo "Waiting for SSL certificates to appear.."
for TLS_DOMAIN in ${IMAP_TLS_DOMAIN}; do
  while [ true ]; do
    if [ -r "/etc/dovecot/tls/certs/${TLS_DOMAIN}/fullchain.pem" ]; then
      break
    fi
    echo "/etc/dovecot/tls/certs/${TLS_DOMAIN}/fullchain.pem does not exist. waiting."
    sleep 2
  done
done
exec /usr/sbin/dovecot -F
