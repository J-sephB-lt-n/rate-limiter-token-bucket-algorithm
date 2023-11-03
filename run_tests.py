"""Run an example test case (user making requests to the API endpoint)"""

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
        f"user_id={user_id}",
        f"request@{request_time}",
        f"response_status_code: {response.status_code}",
        response.text,
    )
    time.sleep(wait_secs)
