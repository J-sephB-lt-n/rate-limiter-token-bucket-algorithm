"""Defines the rate_limit_user.v*() function"""

# standard lib imports #
import time

# project module imports #
import config


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
    # get user request history from local redis db #
    user_request_hist: dict[str, int] = redis_db.hgetall(user_id)

    # add this user to the local redis db if they are not there #
    if not user_request_hist:
        redis_db.hset(
            user_id,
            mapping={
                "n_tokens": config.USER_MAX_N_TOKENS - 1,
                "last_tokens_added_datetime_utc": int(time.time() * 1_000),
            },
        )
        return False

    # if user has token(s), use 1 to process their request #
    if int(user_request_hist["n_tokens"]) > 0:
        redis_db.hincrby(user_id, "n_tokens", -1)
        return False

    # add tokens if sufficient time has passed #
    millisecs_since_last_added_tokens: int = int(time.time() * 1_000) - int(
        user_request_hist["last_tokens_added_datetime_utc"]
    )
    n_tokens_to_add: int = (
        millisecs_since_last_added_tokens // config.TOKEN_ADDED_EVERY_MILLISECS
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
    return False
