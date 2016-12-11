#Docker dovecot

Dovecot IMAP server for my mail domain.

## License

MIT

## Env
    * IMAP_TLS_DOMAIN: tls domain we want to serve over TLS. Only one domain is supported at this time.
    * SEED_USERS: a list of users to inject at run into the userdb. Syntax: domain:user:password. Some characters are not supported ("$", "'" ";")..

## Tests

This project can be tested with testinfra (https://github.com/philpep/testinfra), by running `make test`.

Testinfra is configured to spawn a docker container for each test, and to remove it after.

Launch configuration (environment var) are passed by pytest parameters.

## TODO

  * Test TLS setup
  * Test sieve
  * Test tarpiting (http://wiki2.dovecot.org/Authentication/Penalty )

