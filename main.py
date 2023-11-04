"""
The main entry script, defining the FastAPI endpoint
"""

# 3rd party imports #
from fastapi import FastAPI, HTTPException

# project module imports #
from connect_to_local_redis_db import redis_db
import rate_limit_user

app = FastAPI()


@app.get("/{user_id}")
def does_nothing(user_id):
    """Request which does nothing"""
    if rate_limit_user.v1(user_id, redis_db):
        raise HTTPException(429, "Too Many Requests")

    return {"detail": "OK"}
