import importlib.metadata

__version__ = importlib.metadata.version(__name__)

from .session import Session
from .types import Album, Track
from . import errors

__all__ = ['Session', 'Album', 'Track', 'errors']
