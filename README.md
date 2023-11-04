# rate-limiter-token-bucket-algorithm
An example implementation of the [token-bucket algorithm]() for API rating-limiting, using python, redis and FastAPI.

The concept is very simple: users acquire tokens at a fixed rate (up to a maximum number of tokens) and then consume a single token with each API request. If a user has no tokens at request time, then they receive a **429: Too Many Requests** response to their request. This could be extended to allow for different request sizes to consume different numbers of tokens (or fractions of tokens). 

Start redis database and fastAPI servers in the background:

```bash
redis-server --daemonize yes
nohup uvicorn main:app --port 8000 &
```

Run a simple test case: 

```bash
python run_random_test_case.py
```
```
user_id=joe request@13:14:37 response_status_code: 200 response: OK
user_id=joe request@13:14:38 response_status_code: 200 response: OK
user_id=joe request@13:14:40 response_status_code: 200 response: OK
user_id=joe request@13:14:41 response_status_code: 200 response: OK
user_id=joe request@13:14:43 response_status_code: 200 response: OK
user_id=joe request@13:14:44 response_status_code: 200 response: OK
user_id=joe request@13:14:45 response_status_code: 200 response: OK
user_id=joe request@13:14:46 response_status_code: 200 response: OK
user_id=joe request@13:14:47 response_status_code: 429 response: Too Many Requests
user_id=joe request@13:14:49 response_status_code: 200 response: OK
user_id=joe request@13:14:49 response_status_code: 429 response: Too Many Requests
user_id=joe request@13:14:50 response_status_code: 429 response: Too Many Requests
user_id=joe request@13:14:50 response_status_code: 429 response: Too Many Requests
user_id=joe request@13:14:51 response_status_code: 429 response: Too Many Requests
user_id=joe request@13:14:52 response_status_code: 200 response: OK
user_id=joe request@13:14:54 response_status_code: 429 response: Too Many Requests
user_id=joe request@13:14:54 response_status_code: 429 response: Too Many Requests
user_id=joe request@13:14:54 response_status_code: 429 response: Too Many Requests
user_id=joe request@13:14:56 response_status_code: 200 response: OK
user_id=joe request@13:14:57 response_status_code: 429 response: Too Many Requests
```

Stop the redis database and fastAPI servers, and clean up:

```bash
redis-cli shutdown
rm dump.rdb
UVICORN_PID=$(pgrep -f "uvicorn main:app")
kill -15 $UVICORN_PID
rm nohup.out
```