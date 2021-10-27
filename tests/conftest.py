import sys

if sys.version_info < (3,):
    # Python async syntax is in Py3 only
    collect_ignore_glob = ["*_async.py"]
