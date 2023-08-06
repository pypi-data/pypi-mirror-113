"""
Fabric tasks

Default environments is `dev`, `test`, `prod`

"""
import os
from fabric import task, Config


@task
def hi(c):
    print(f'Hi, DevOps with Fabric is ready! {c.host}')


@task
def deploy(c):
    """Deploy"""
    config = Config()
    print('From Configuration files (yaml), debug: %s' % os.getenv('debug'))
    print('From Configuration files (yaml), fabric_debug: %s' % os.getenv('fabric_debug'))
    print('From Configuration files (yaml), FABRIC_DEBUG: %s' % os.getenv('FABRIC_DEBUG'))
    print('From Configuration files (yaml), INVOKE_DEBUG: %s' % os.getenv('INVOKE_DEBUG'))
    print('From Configuration files (yaml), config INVOKE_DEBUG: %s' % config['debug'])
    # c.run('uname -s')
