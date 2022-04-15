"""Core project features."""
from .config import Settings, get_settings

cached_settings: Settings = get_settings()
