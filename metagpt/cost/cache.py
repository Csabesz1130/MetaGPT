#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/4/4
@Author  : Gemini
@File    : cache.py
"""

import time
import hashlib
from typing import Optional, Any, Dict

class CachingSystem:
    """Caches AI responses to reduce redundant API calls."""

    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        Initializes the CachingSystem.

        Args:
            max_size (int): Maximum number of items to store in the cache.
            default_ttl (int): Default time-to-live for cache entries in seconds.
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._keys_by_time = [] # Helper list to manage eviction

    def _generate_key(self, prompt: str, endpoint: str, **kwargs) -> str:
        """Generates a unique cache key based on prompt, endpoint, and other parameters."""
        key_material = f"{endpoint}:{prompt}:{str(sorted(kwargs.items()))}"
        return hashlib.sha256(key_material.encode()).hexdigest()

    def get(self, prompt: str, endpoint: str, **kwargs) -> Optional[Any]:
        """Retrieves an item from the cache if it exists and hasn't expired."""
        key = self._generate_key(prompt, endpoint, **kwargs)
        entry = self.cache.get(key)
        if entry:
            if time.time() < entry['expires_at']:
                # Optionally update access time for LRU eviction
                return entry['value']
            else:
                # Expired entry, remove it
                self._remove_entry(key)
        return None

    def set(self, prompt: str, endpoint: str, value: Any, ttl: Optional[int] = None, **kwargs):
        """Adds an item to the cache."""
        if len(self.cache) >= self.max_size:
            self._evict()
            
        key = self._generate_key(prompt, endpoint, **kwargs)
        expires_at = time.time() + (ttl if ttl is not None else self.default_ttl)
        self.cache[key] = {'value': value, 'expires_at': expires_at, 'added_at': time.time()}
        self._keys_by_time.append((expires_at, key))
        self._keys_by_time.sort() # Keep sorted for efficient eviction

    def _evict(self):
        """Evicts the oldest or least recently used item(s) from the cache."""
        # Simple time-based eviction (oldest first)
        if self._keys_by_time:
            _, oldest_key = self._keys_by_time.pop(0)
            self._remove_entry(oldest_key)
        # Could implement LRU here by tracking access times
            
    def _remove_entry(self, key: str):
      """Removes a specific entry from the cache and the time list."""
      if key in self.cache:
          del self.cache[key]
          # Remove from _keys_by_time (less efficient without a lookup dict)
          self._keys_by_time = [(t, k) for t, k in self._keys_by_time if k != key]

    def clear(self):
        """Clears the entire cache."""
        self.cache.clear()
        self._keys_by_time.clear()
        
    def get_size(self) -> int:
        """Returns the current number of items in the cache."""
        return len(self.cache) 