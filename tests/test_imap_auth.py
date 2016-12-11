import pytest
from imaplib import IMAP4
@pytest.mark.auth
@pytest.mark.parametrize("Docker", [
    { "users": [("abc", "def.fr", "toto")] },
    { "users": [("abc", "def.fr", "toto"), ("abc2", "def.fr2", "toto2"),("abc3", "def.fr3", "toto3")] },
    { "users": [("special_char", "domain.eu", "-L5@S>C.1A^I(")]},
    ], indirect=True)
@pytest.mark.auth
def test_imap_auth(Docker):
    for user, domain, password in Docker.args.get('users'):
        imap = IMAP4(Docker.get_ip())
        imap.login(user+"@"+domain, password)
        imap.logout()

@pytest.mark.auth
@pytest.mark.parametrize("Docker", [
    { "users": [("special_char_!$", "domain.eu", "-$L5@S>C.1A^I(")]},
    { "users": [("long_username_is_loooooooooooooooooooooooog", "domain.eu", "blah")]},
    ], indirect=True)
def test_imap_invalid_char_auth(Docker):
    for user, domain, password in Docker.args.get('users'):
        try:
            imap = IMAP4(Docker.get_ip())
            imap.login(user+"@"+domain, password)
            imap.logout()
        except IMAP4.error as err:
            assert err.message == "[AUTHENTICATIONFAILED] Authentication failed."
