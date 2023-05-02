from redis.asyncio import Redis

from client import AsyncRedisClient
from core import settings
from storage import AsyncRedisStorage

redis_dsn = settings.redis_dsn
redis = AsyncRedisClient(Redis(host=redis_dsn.host, port=int(redis_dsn.port), db=redis_dsn.path[1:]))
storage = AsyncRedisStorage(redis)
