"""
Abstract base models for the collaborative document editing platform.
Provides common functionality for datetime tracking and caching.
"""
from django.db import models


class AbstractDateTimeModel(models.Model):
    """
    Abstract base model that provides datetime tracking fields.
    Use this for models that don't need caching.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-updated_at']


class AbstractDateTimeCacheModel(AbstractDateTimeModel):
    """
    Abstract base model that provides datetime tracking and caching functionality.
    Use this for models that need caching with 2-hour TTL.
    
    Cached operations: get, exist, filter
    TTL: 2 hours (7200 seconds)
    """
    
    class Meta:
        abstract = True
        ordering = ['-updated_at']
    
