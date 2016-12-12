import pytest
from imaplib import IMAP4
import smtplib
@pytest.mark.lmtp
@pytest.mark.parametrize("Docker", [
    { "users": [("abc", "def.fr", "toto")] },
    { "users": [("abc", "def.fr", "toto"), ("abc2", "def.fr2", "toto2"),("abc3", "def.fr3", "toto3")] },
    { "users": [("special_char", "domain.eu", "-L5@S>C.1A^I(")]},
    ], indirect=True)
def test_lmtp_delivery(Docker):
    for user, domain, password in Docker.args.get('users'):
        lmtp = smtplib.LMTP(Docker.get_ip(), 24)
        lmtp.sendmail('test@example.invalid', user+"@"+domain, "test")
        lmtp.sendmail('test@example.invalid', user+"+plusaddressing@"+domain, "test")

@pytest.mark.lmtp
@pytest.mark.parametrize("Docker", [
    { "users": [("abc", "def.fr", "toto")] },
    ], indirect=True)
def test_lmtp_delivery_and_fetch(Docker):
    for user, domain, password in Docker.args.get('users'):
        lmtp = smtplib.LMTP(Docker.get_ip(), 24)
        lmtp.sendmail('test@example.invalid', user+"@"+domain, "test")
        imap = IMAP4(Docker.get_ip())
        imap.login(user+"@"+domain, password)
        imap.select("INBOX")
        typ, data = imap.search(None, 'ALL')
        num = data[0].split()[-1]
        rv = imap.fetch(num, '(BODY[TEXT])')[0]
        assert rv == "OK"
        imap.logout()

@pytest.mark.lmtp
@pytest.mark.parametrize("Docker", [
    { "users": [("abc", "def.fr", "toto")] },
    { "users": [("invalid2", "example.invalid", "toto")] },
    { "users": [("inva", "example.invalid", "toto")] },
    ], indirect=True)
def test_lmtp_delivery_invalid_user(Docker):
    lmtp = smtplib.LMTP(Docker.get_ip(), 24)
    try:
        lmtp.sendmail('test@example.invalid', "invalid@example.invalid", "test")
    except smtplib.SMTPRecipientsRefused as err:
        assert err.message == ""
