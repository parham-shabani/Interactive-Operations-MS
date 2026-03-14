"""
Initializer for the redis_cache package.

Exposes a utility function `get_manager()` which automatically returns
an appropriate Redis manager (sync or async) based on the execution context.
Useful for shared or abstracted Redis access across different environments.
"""

import asyncio
from core.redis_cache.redis_manager_sync import RedisSyncManager
from core.redis_cache.redis_manager_async import RedisAsyncManager


class RedisManagerAuto:
    """
    Automatically selects the appropriate Redis manager (sync or async)
    based on the current execution context.

    This class creates internal instances of both RedisSyncManager and RedisAsyncManager.
    When `get_manager()` is called, it inspects the context (via asyncio) and returns
    the correct manager for use.

    Use this when you want to write shared code without worrying about sync/async differences.
    """

    def __init__(self):
        """
        initialize both sync and async Redis managers.
        """
        self._sync = RedisSyncManager()
        self._async = RedisAsyncManager()

    def get_manager(self):
        """
        Determine the current execution context.

        Returns:
            RedisAsyncManager: if running in an async event loop.
            RedisSyncManager: if running in a sync/blocking context.

        Raises:
            None – falls back to sync mode if no event loop is detected.
        """
        try:
            asyncio.get_running_loop()
            return self._async
        except RuntimeError:
            return self._sync


# Example usage for importing Redis manager dynamically
redis_manager = RedisManagerAuto()

# Usage in other parts of the project:
# from core.redis_cache import redis_manager
# Sync context:
# data = redis_manager.get_manager().get("some_key")
# Async context:
# data = await redis_manager.get_manager().get("some_key")


redis_manager_async = RedisAsyncManager()
redis_manager_sync = RedisSyncManager()
