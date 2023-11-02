"""
docstring TODO
"""
# standard lib imports #

# 3rd party imports #
from fastapi import FastAPI, HTTPException

# project module imports #
from connect_to_local_redis_db import redis_db
import rate_limit_user

app = FastAPI()


@app.get("/{user_id}")
def process_get_request(user_id):
    """docstring TODO"""
    if rate_limit_user.v1(user_id, redis_db):
        raise HTTPException(429, "Too Many Requests")

    return redis_db.hget(user_id, "n_tokens")
