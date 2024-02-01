#!/usr/bin/python3
""" Function that deploys """
from fabric.api import *


env.hosts = ["100.25.171.37", "3.85.175.199"]
env.user = "ubuntu"


def do_clean(number=0):
    """ delete archives """

    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
