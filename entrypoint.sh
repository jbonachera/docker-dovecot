#!/bin/bash
trap 'exit' INT
if [ -n "$IMAP_TLS_DOMAIN" ]; then
  sed -i "s/@@IMAP_TLS_DOMAIN@@/${IMAP_TLS_DOMAIN}/g" /etc/dovecot/conf.d/*
  
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
fi
exec /usr/sbin/dovecot -F
