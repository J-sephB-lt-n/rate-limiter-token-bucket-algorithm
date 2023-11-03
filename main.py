"""
The main entry script, defining the FastAPI endpoint
"""

# standard lib imports #

# 3rd party imports #
from fastapi import FastAPI, HTTPException

# project module imports #
from connect_to_local_redis_db import redis_db
import rate_limit_user

app = FastAPI()


@app.get("/{user_id}")
def count_tokens(user_id):
    """Tells a user how many tokens are left in their bucket
    (after removing 1 token for calling this endpoint)
    """
    if rate_limit_user.v1(user_id, redis_db):
        raise HTTPException(429, "Too Many Requests")

    return {"n_tokens": int(redis_db.hget(user_id, "n_tokens"))}
