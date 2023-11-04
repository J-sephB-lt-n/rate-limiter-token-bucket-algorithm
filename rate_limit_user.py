"""Defines the rate_limit_user.v*() function"""

# standard lib imports #
import json
import logging
import time

# project module imports #
import config

# set up logger #
logger = logging.getLogger(__name__)


def v1(user_id: str, redis_db) -> bool:
    """Rate limits a user using the token-bucket algorithm
    (also changing the state of the local redis db)

    Returns
    -------
    bool
        True
            if user request should be blocked (rate-limited)
        False
            if user request shouldn't be blocked (rate-limited)
    """
    logger.debug(
        "getting user request history from local redis db: user_id='%s'", user_id
    )
    user_request_hist: dict[str, int] = redis_db.hgetall(user_id)
    logger.debug(json.dumps(user_request_hist, indent=4))  # log user entry in redis

    if not user_request_hist:
        logger.info(
            "user_id='%s' does not exist in redis database: adding user to redis database",
            user_id,
        )
        redis_db.hset(
            user_id,
            mapping={
                "n_tokens": config.USER_MAX_N_TOKENS - 1,
                "last_tokens_added_datetime_utc": int(time.time() * 1_000),
            },
        )
        logger.debug(json.dumps(redis_db.hgetall(user_id), indent=4))  # user in redis
        return False

    if int(user_request_hist["n_tokens"]) > 0:
        logger.debug("consuming 1 token to service request: user_id='%s'", user_id)
        redis_db.hincrby(user_id, "n_tokens", -1)
        logger.debug(json.dumps(redis_db.hgetall(user_id), indent=4))  # user in redis
        return False

    logger.debug(
        "user has no tokens available to process request: user_id='%s'", user_id
    )

    # add tokens if sufficient time has passed #
    millisecs_since_last_added_tokens: int = int(time.time() * 1_000) - int(
        user_request_hist["last_tokens_added_datetime_utc"]
    )
    n_tokens_to_add: int = (
        millisecs_since_last_added_tokens // config.TOKEN_ADDED_EVERY_MILLISECS
    )
    logger.debug(
        "adding %s token(s) to user_id='%s'",
        min(n_tokens_to_add, config.USER_MAX_N_TOKENS),
        user_id,
    )

    # block user request if no tokens available #
    if n_tokens_to_add == 0:
        return True

    redis_db.hset(
        user_id,
        mapping={
            "n_tokens": min(n_tokens_to_add, config.USER_MAX_N_TOKENS) - 1,
            "last_tokens_added_datetime_utc": int(
                user_request_hist["last_tokens_added_datetime_utc"]
            )
            + (n_tokens_to_add * config.TOKEN_ADDED_EVERY_MILLISECS),
        },
    )
    logger.debug(json.dumps(redis_db.hgetall(user_id), indent=4))  # user in redis
    return False
