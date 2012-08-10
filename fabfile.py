import time

from fabric.api import env, local, prefix, require, run, settings, sudo, task
from fabric.colors import cyan, green, red

@task
def install():
    """Installs everything from top to bottom."""
    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
    sudo('cat deb http://downloads-distro.mongodb.org/repo/debian-sysvinit dist 10gen >> /etc/apt/sources.list.d/10gen.list')
    sudo('aptitude update')
    sudo('aptitude install mongodb python python-dev')
    run('curl -s https://raw.github.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL')
    run('mkvirtualenv gtproxy')
    # only if we are remote
    run('git clone ssh://git@talpor.com:22022/gtproxy.git')

@task
def deploy():
    run('git pull')
    with prefix('workon gtproxy'):
        run('pip install -r requirements.pip')
        # only if we are remote
        with settings(warn_only=True):
            run('supervisorctl shutdown')
        run('supervisord')
        time.sleep(1)  # lets wait a little so gunicorn restarts
        check()

def check():
    """Check that the home page of the site returns an HTTP 200."""
    require('site_url')
    print(cyan('Checking site status...', bold=True))

    if not '200 OK' in local('curl --silent -I "%s"' % env.site_url, capture=True):
        _sad()
    else:
        _happy()


# HELPERS
# ------------------------------------------------------------------------------

def _happy():
    print(green('\nLooks good from here!\n'))

def _sad():
    print(red(r"""
          ___           ___
         /  /\         /__/\
        /  /::\        \  \:\
       /  /:/\:\        \__\:\
      /  /:/  \:\   ___ /  /::\
     /__/:/ \__\:\ /__/\  /:/\:\
     \  \:\ /  /:/ \  \:\/:/__\/
      \  \:\  /:/   \  \::/
       \  \:\/:/     \  \:\
        \  \::/       \  \:\
         \__\/         \__\/
          ___           ___     
         /__/\         /  /\     ___
         \  \:\       /  /::\   /__/\
          \  \:\     /  /:/\:\  \  \:\
      _____\__\:\   /  /:/  \:\  \  \:\
     /__/::::::::\ /__/:/ \__\:\  \  \:\
     \  \:\~~\~~\/ \  \:\ /  /:/   \  \:\
      \  \:\  ~~~   \  \:\  /:/     \__\/
       \  \:\        \  \:\/:/          __
        \  \:\        \  \::/          /__/\
         \__\/         \__\/           \__\/

         Something seems to have gone wrong!
         You should probably take a look at that.
    """))
