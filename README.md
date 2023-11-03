# rate-limiter-token-bucket-algorithm
An example implementation of the [token-bucket algorithm]() for API rating-limiting, using python, redis and FastAPI.

The concept is very simple: users acquire tokens at a fixed rate (up to a maximum amount), and then consume a token with each API request. If they have insufficient tokens available, then they receive a **429: Too Many Requests** response to their request. The method can be extended to allow for different request sizes to consume different numbers of tokens.

Start redis database and fastAPI servers in the background:

```bash
redis-server --daemonize yes
nohup uvicorn main:app --port 8000 &
```

Run a simple test: 

```bash
python run_tests.py
```
```
user_id=joe request@09:26:30 response_status_code: 200 {"n_tokens":5}
user_id=joe request@09:26:31 response_status_code: 200 {"n_tokens":4}
user_id=joe request@09:26:32 response_status_code: 200 {"n_tokens":3}
user_id=joe request@09:26:33 response_status_code: 200 {"n_tokens":3}
user_id=joe request@09:26:33 response_status_code: 200 {"n_tokens":2}
user_id=joe request@09:26:33 response_status_code: 200 {"n_tokens":1}
user_id=joe request@09:26:33 response_status_code: 200 {"n_tokens":0}
user_id=joe request@09:26:34 response_status_code: 429 {"detail":"Too Many Requests"}
user_id=joe request@09:26:41 response_status_code: 200 {"n_tokens":1}
user_id=joe request@09:26:46 response_status_code: 200 {"n_tokens":1}
user_id=joe request@09:26:47 response_status_code: 200 {"n_tokens":0}
user_id=joe request@09:26:48 response_status_code: 429 {"detail":"Too Many Requests"}
user_id=joe request@09:26:49 response_status_code: 200 {"n_tokens":0}
user_id=joe request@09:26:50 response_status_code: 429 {"detail":"Too Many Requests"}
```

Stop the redis database and fastAPI servers:

```bash
redis-cli shutdown
rm dump.rdb
UVICORN_PID=$(pgrep -f "uvicorn main:app")
kill -15 $UVICORN_PID
rm nohup.out
```