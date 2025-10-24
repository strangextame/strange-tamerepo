"""
Configuration for the MTG Card Finder Flask Application.

This file centralizes configuration variables, allowing for different settings
for development, testing, and production environments. It loads settings from
environment variables to avoid hardcoding sensitive or environment-specific data.
"""

import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-very-secret-key-that-you-should-change')
    DEBUG = False
    TESTING = False
    SCRYFALL_API_BASE_URL = "https://api.scryfall.com"

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True