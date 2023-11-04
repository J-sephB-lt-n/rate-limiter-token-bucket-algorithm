"""Run a random test case (user making multiple requests to the API endpoint)"""

# standard lib imports #
import datetime
import random
import time

# 3rd party imports #
import requests

# run the test
for _ in range(20):
    user_id: str = "joe"
    request_time: str = datetime.datetime.now().strftime("%H:%M:%S")
    response = requests.get(f"http://localhost:8000/{user_id}", timeout=5)
    print(
        f"user_id={user_id}",
        f"request@{request_time}",
        f"response_status_code: {response.status_code}",
        f'response: {response.json()["detail"]}',
    )
    time.sleep(random.uniform(0, 2))
