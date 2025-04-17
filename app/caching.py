import redis
from redis.exceptions import ConnectionError, RedisError
import logging
from typing import Optional, Any
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self, settings):
        self.settings = settings
        self.client = self._create_client()
        
    def _create_client(self) -> Optional[redis.Redis]:
        try:
            return redis.Redis(
                host=self.settings.REDIS_HOST,
                port=self.settings.REDIS_PORT,
                db=self.settings.REDIS_DB,
                password=self.settings.REDIS_PASSWORD,
                socket_timeout=5,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
        except Exception as e:
            logger.error(f"Failed to create Redis client: {str(e)}")
            return None
            
    def get(self, key: str) -> Optional[Any]:
        try:
            if not self.client:
                return None
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Error getting key {key}: {str(e)}")
            return None
            
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        try:
            if not self.client:
                return False
            return self.client.setex(
                key,
                expire,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Error setting key {key}: {str(e)}")
            return False

class MemoryCache:
    def __init__(self):
        self._cache = {}
        
    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)
        
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        self._cache[key] = value
        return True

class DiskCache:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
        
    def get(self, key: str) -> Optional[Any]:
        try:
            cache_file = self.cache_dir / f"{key}.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error reading from disk cache: {str(e)}")
            return None
            
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        try:
            cache_file = self.cache_dir / f"{key}.json"
            with open(cache_file, 'w') as f:
                json.dump(value, f)
            return True
        except Exception as e:
            logger.error(f"Error writing to disk cache: {str(e)}")
            return False

class CacheManager:
    def __init__(self, settings):
        self.settings = settings
        self.redis = RedisCache(settings)
        self.memory = MemoryCache()
        self.disk = DiskCache(settings.STORAGE_DIR / "cache")
        
    def get(self, key: str) -> Optional[Any]:
        """Get value with multi-level caching"""
        # Try memory cache first
        value = self.memory.get(key)
        if value is not None:
            return value
            
        # Try Redis cache
        value = self.redis.get(key)
        if value is not None:
            self.memory.set(key, value)
            return value
            
        # Try disk cache
        value = self.disk.get(key)
        if value is not None:
            self.memory.set(key, value)
            self.redis.set(key, value)
            return value
            
        return None
        
    def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in all cache levels"""
        success = True
        
        # Set in memory cache
        if not self.memory.set(key, value, expire):
            success = False
            
        # Set in Redis cache
        if not self.redis.set(key, value, expire):
            success = False
            
        # Set in disk cache
        if not self.disk.set(key, value, expire):
            success = False
            
        return success 