#!/usr/bin/python3
""" Fabric script that deploys archive"""
from datetime import datetime
from fabric.api import *
import os

env.hosts = ["100.25.171.37", "3.85.175.199"]
env.user = "ubuntu"


def do_pack():
    """Compressing files"""
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        t = datetime.now()
        f = "%Y%m%d%H%M%S"
        path = 'versions/web_static_{}.tgz'.format(t.strftime(f))
        local('tar -cvzf {} web_static'.format(path))
        return path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """Deploying files"""
    if os.path.exists(archive_path):
        wiext = archive_path[9:]
        woext = "/data/web_static/releases/" + wiext[:-4]
        wiext = "/tmp/" + wiext
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(woext))
        run("sudo tar -xzf {} -C {}/".format(wiext,
                                             woext))
        run("sudo rm {}".format(wiext))
        run("sudo mv {}/web_static/* {}".format(woext,
                                                woext))
        run("sudo rm -rf {}/web_static".format(woext))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(woext))

        print("New version deployed!")
        return True

    return False


def deploy():
    """Full deployment"""
    creat_arch = do_pack()
    if creat_arch is None:
        return False
    return do_deploy(creat_arch)
