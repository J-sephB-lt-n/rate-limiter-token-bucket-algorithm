"""Constants which control the behaviour of the project"""

import logging
from typing import Final

LOGGING_LEVEL: Final[int] = logging.DEBUG
TOKEN_ADDED_EVERY_MILLISECS: Final[int] = 3_000
USER_MAX_N_TOKENS: Final[int] = 5  # user cannot have more tokens than this
