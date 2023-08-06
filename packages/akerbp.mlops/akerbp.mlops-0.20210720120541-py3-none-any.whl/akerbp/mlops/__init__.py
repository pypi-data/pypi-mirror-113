try:
    from importlib.metadata import version
    __version__ = version('akerbp.mlops')
except:
   __version__ = 'unknown' 