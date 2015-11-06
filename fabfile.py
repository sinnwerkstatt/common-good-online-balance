from fabric.api import *
from fabvenv import virtualenv


def staging():
    env.hosts = ['ecg@server.sinnwerkstatt.com']
    env.path = '/srv/ecg.sinnwerkstatt.com/ecg-balancing'
    env.push_branch = 'master'
    env.push_remote = 'github'
    env.virtualenv_path = '/srv/ecg.sinnwerkstatt.com/ecgenv'


def production():
    env.hosts = ['deploy_hosts_user@example.com']
    env.path = '/var/www/vhosts/example.com/httpdocs'
    env.push_branch = 'master'
    env.push_remote = 'origin'
    env.virtualenv_path = '/var/www/vhosts/example.com/ecg_balancingenv/'


def update():
    with cd(env.path):
        run("git pull %(push_remote)s %(push_branch)s" % env)


def pip():
    update()
    with cd(env.path):
        with virtualenv(env.virtualenv_path):
            run("pip install -Ur requirements.txt ")


def deploy():
    update()
    with cd(env.path):
        with virtualenv(env.virtualenv_path):
            run("python manage.py syncdb")
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")
            run("supervisorctl restart ecg")


def syncdb():
    with cd(env.path):
        run("cat ecg_balancing_dump.sql | mysql -uecg_balancing ecg_balancing")
