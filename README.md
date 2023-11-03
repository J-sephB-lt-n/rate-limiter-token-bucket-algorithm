# rate-limiter-token-bucket-algorithm
An example implementation of the token-bucket algorithm for API rating limiting, using python, redis and FastAPI

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
user_id=joe request@09:12:13 response_status_code: 200 {"n_tokens":5}
user_id=joe request@09:12:14 response_status_code: 200 {"n_tokens":4}
user_id=joe request@09:12:15 response_status_code: 200 {"n_tokens":3}
user_id=joe request@09:12:16 response_status_code: 200 {"n_tokens":2}
user_id=joe request@09:12:16 response_status_code: 200 {"n_tokens":1}
user_id=joe request@09:12:16 response_status_code: 200 {"n_tokens":0}
user_id=joe request@09:12:16 response_status_code: 429 {"detail":"Too Many Requests"}
user_id=joe request@09:12:17 response_status_code: 429 {"detail":"Too Many Requests"}
user_id=joe request@09:12:24 response_status_code: 200 {"n_tokens":2}
user_id=joe request@09:12:29 response_status_code: 200 {"n_tokens":3}
user_id=joe request@09:12:30 response_status_code: 200 {"n_tokens":2}
user_id=joe request@09:12:31 response_status_code: 200 {"n_tokens":1}
user_id=joe request@09:12:32 response_status_code: 200 {"n_tokens":0}
user_id=joe request@09:12:33 response_status_code: 429 {"detail":"Too Many Requests"}
```

Stop the redis database and fastAPI servers:

```bash
redis-cli shutdown
rm dump.rdb
UVICORN_PID=$(pgrep -f "uvicorn main:app")
kill -15 $UVICORN_PID
rm nohup.out
```