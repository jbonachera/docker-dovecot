def test_dovecot_running(Docker):
    assert Docker.backend.get_module("Process").get(comm="dovecot", user="root")
def test_dovecot_auth_running(Docker):
    assert Docker.backend.get_module("Process").get(comm="auth", user="dovecot")
def test_dovecot_anvil_running(Docker):
    assert Docker.backend.get_module("Process").get(comm="anvil", user="dovecot")

