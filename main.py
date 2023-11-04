"""
The main entry script, defining the FastAPI endpoint
"""

# standard lib imports #
import config
import logging

# 3rd party imports #
from fastapi import FastAPI, HTTPException

# project module imports #
from connect_to_local_redis_db import redis_db
import rate_limit_user

# set up logging #
logging.basicConfig(
    level=config.LOGGING_LEVEL,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/{user_id}")
def does_nothing(user_id):
    """Request which does nothing"""
    logger.info("initiated request: user_id='%s'", user_id)

    if rate_limit_user.v1(user_id, redis_db):
        logger.info("rejected request: user_id='%s'", user_id)
        raise HTTPException(429, "Too Many Requests")

    logger.info("accepted request: user_id='%s'", user_id)
    return {"detail": "OK"}
