import sys

if sys.version_info >= (3, 8):
    import importlib.metadata as importlib_metadata
else:
    import importlib_metadata

version = importlib_metadata.version("manifestoo")
core_version = importlib_metadata.version("manifestoo_core")
