"""Set up connection to local REDIS database"""

import redis

redis_db = redis.Redis(host="localhost", port=6379, decode_responses=True)
redis_db.config_set("maxmemory", "100mb")  # discard data after reaching this db size
redis_db.config_set("maxmemory-policy", "allkeys-lru")  # discard oldest data first
