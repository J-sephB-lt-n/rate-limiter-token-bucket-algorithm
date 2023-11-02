"""docstring TODO"""

import datetime
import time
import requests

for user_id, wait_secs in (
    ("joe", 1),
    ("joe", 1),
    ("joe", 1),
    ("joe", 0),
    ("joe", 0),
    ("joe", 0),
    ("joe", 1),
    ("joe", 7),
    ("joe", 5),
    ("joe", 1),
    ("joe", 1),
    ("joe", 1),
    ("joe", 1),
    ("joe", 1),
):
    request_time: str = datetime.datetime.now().strftime("%H:%M:%S")
    response = requests.get(f"http://localhost:8000/{user_id}")
    print(
        "user_id=" + user_id,
        "request at " + request_time,
        "response code: " + str(response.status_code),
        "n_tokens: " + response.text,
    )
    time.sleep(wait_secs)
