import importlib.metadata

__version__ = importlib.metadata.version(__name__)

from . import types, utils, consts, errors, session
from .session import Session
from .types import Album, Track

__all__ = ['Session', 'Album', 'Track', 'errors',
           'utils', 'consts', 'types', 'session']
