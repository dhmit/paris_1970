try:
    from .settings import *
except ImportError as e:
    if e.msg == "No module named 'config.settings.settings'":
        from .dev import *
    else:
        raise
