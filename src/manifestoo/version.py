try:
    import importlib.metadata as importlib_metadata
except ImportError:
    import importlib_metadata

version = importlib_metadata.version("manifestoo")
