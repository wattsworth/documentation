import sys

def on_config(config):
    joule_modules = [name for name in sys.modules if name.startswith("joule")]
    for module in joule_modules:
        del sys.modules[module]