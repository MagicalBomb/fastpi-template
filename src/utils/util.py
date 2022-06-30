import importlib


def try_import(module):
    try:
        return importlib.import_module(module)
    except ImportError:
        pass

