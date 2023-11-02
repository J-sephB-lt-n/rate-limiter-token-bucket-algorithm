"""docstring TODO"""

# standard lib imports #
import time

# project module imports #
import config


def v1(user_id: str, redis_db) -> bool:
    """docstring TODO"""
    user_request_hist: dict[str, int] = redis_db.hgetall(user_id)
    if not user_request_hist:
        redis_db.hset(
            user_id,
            mapping={
                "n_tokens": config.USER_MAX_N_TOKENS,
                "request_datetime_utc": int(time.time()),
            },
        )
        return False
    current_datetime_utc: int = int(time.time())
    n_tokens_to_add: int = int(
        (current_datetime_utc - int(user_request_hist["request_datetime_utc"]))
        / config.TOKEN_ADD_N_SECS
    )
    if n_tokens_to_add == 0 and int(user_request_hist["n_tokens"]) < 1:
        redis_db.hset(
            user_id,
            mapping={
                "n_tokens": 0,
                "request_datetime_utc": current_datetime_utc,
            },
        )
        return True

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
