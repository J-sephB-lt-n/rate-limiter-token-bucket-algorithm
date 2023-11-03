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
        True if user request must be blocked (rate-limited)
        False if the user request need not be blocked (rate-limited)
    """
    # get user request history from local redis db #
    user_request_hist: dict[str, int] = redis_db.hgetall(user_id)

    current_datetime_utc: int = int(time.time())

    # add this user to the local redis db if they are not there #
    if not user_request_hist:
        redis_db.hset(
            user_id,
            mapping={
                "n_tokens": config.USER_MAX_N_TOKENS,
                "request_datetime_utc": current_datetime_utc,
                "last_token_added_datetime_utc": current_datetime_utc,
            },
        )
        return False

    # add tokens if sufficient time has passed #
    n_tokens_to_add: int = int(
        (current_datetime_utc - int(user_request_hist["last_token_added_datetime_utc"]))
        / config.TOKEN_ADD_N_SECS
    )

    # rate-limit user if they do not have enough tokens #
    if n_tokens_to_add == 0 and int(user_request_hist["n_tokens"]) < 1:
        redis_db.hset(
            user_id,
            mapping={
                "n_tokens": 0,
                "request_datetime_utc": current_datetime_utc,
            },
        )
        return True

    # update user token count after consuming a token #
    if n_tokens_to_add > 0:
        redis_db.hset(
            user_id,
            mapping={
                "n_tokens": min(
                    int(user_request_hist["n_tokens"]) - 1 + n_tokens_to_add,
                    config.USER_MAX_N_TOKENS,
                ),
                "request_datetime_utc": current_datetime_utc,
                "last_token_added_datetime_utc": current_datetime_utc,
            },
        )
    else:
        redis_db.hset(
            user_id,
            mapping={
                "n_tokens": min(
                    int(user_request_hist["n_tokens"]) - 1 + n_tokens_to_add,
                    config.USER_MAX_N_TOKENS,
                ),
                "request_datetime_utc": current_datetime_utc,
            },
        )
    return False
