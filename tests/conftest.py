import pytest
import testinfra
import time
from imaplib import IMAP4
import json

check_output = testinfra.get_backend(
    "local://"
).get_module("Command").check_output


@pytest.fixture()
def Docker(request):
    docker = DockerInstance(request)
    def teardown():
        check_output("docker rm -f %s", docker.docker_id)
    request.addfinalizer(teardown)
    return docker

class DockerInstance:
    def __init__(self, request):
        env = ''
        if hasattr(request, 'param'):
            self.args = request.param
            if 'users' in request.param:
                env += '-e "SEED_USERS='
                tmp_env = ''
                for user, domain, password in request.param.get('users'):
                    tmp_env += '%s:%s:%s ' % (domain, user, password)
                tmp_env.strip()
                tmp_env += '"'
                env += tmp_env
        docker_id = check_output("docker run --health-interval=2s -d %s nsmaster" % env)
        self.docker_id = docker_id
        while True:
            health =json.loads(check_output("docker inspect --format='{{json .State.Health}}' %s" % docker_id))
            time.sleep(1)
            if health['Status'] == 'healthy':
                break
        self.backend = testinfra.get_backend("docker://" + docker_id)

    def get_ip(self):
        return check_output(
            "docker inspect --format '{{ .NetworkSettings.IPAddress }}' %s",
            self.docker_id)
    
