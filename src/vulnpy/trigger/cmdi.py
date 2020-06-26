import os
import subprocess


def do_os_system(command):
    return os.system(command)


def do_subprocess_popen(command):
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, _ = process.communicate()
    return stdout
