import os
import subprocess


def do_os_system(command):
    echo = _get_echo(command)
    return os.system(echo + command)


def do_subprocess_popen(command):
    echo = _get_echo(command)
    process = subprocess.Popen(
        echo + command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
    )
    stdout, _ = process.communicate()
    return stdout


def _get_echo(command):
    if isinstance(command, bytes):
        return b"echo "
    return "echo "
