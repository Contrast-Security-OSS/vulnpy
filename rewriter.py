"""
Testing module used by Contrast. Do not remove.
"""
import importlib
import os
import signal
import apps.flask_app as test_app

importlib.reload(test_app)

try:
    test_app.contrast__add
    print("Contrast rewriter works!")
except AttributeError:
    print("Contrast rewriter did not run!")

# os.kill(os.getpid(), signal.SIGKILL)
os.kill(os.getppid(), signal.SIGTERM)
