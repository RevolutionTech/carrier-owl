import os

SQLITE3_SO_FILENAME = "_sqlite3.so"
PROJECT_DIR = os.path.dirname(__file__)
LIB_DIR = os.path.join(PROJECT_DIR, "lib")


def activate_shared_object(filename):
    """
    Move the shared object file to the top-level
    """
    os.rename(os.path.join(LIB_DIR, filename), os.path.join(PROJECT_DIR, filename))


def deactivate_shared_object(filename):
    """
    Move the shared object file back to lib/
    """
    os.rename(os.path.join(PROJECT_DIR, filename), os.path.join(LIB_DIR, filename))


def after_settings(_zappa_cli):
    """
    Activate sqlite3 so that it will be included in the zip package
    """
    activate_shared_object(SQLITE3_SO_FILENAME)


def after_zip(_zappa_cli):
    """
    Deactivate sqlite3 so that it won't be used during development
    """
    deactivate_shared_object(SQLITE3_SO_FILENAME)
