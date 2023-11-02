# rate-limiter-token-bucket-algorithm
An example implementation of the token-bucket algorithm for API rating limiting, using python, redis and FastAPI

Start redis database and fastAPI servers in the background:

```bash
redis-server --daemonize yes
nohup uvicorn host_api:app --port 8000 &
```

```bash
python run_tests.py
```
```
user_id=joe request at 23:39:16 response code: 200 n_tokens: "5"
user_id=joe request at 23:39:17 response code: 200 n_tokens: "4"
user_id=joe request at 23:39:18 response code: 200 n_tokens: "3"
user_id=joe request at 23:39:19 response code: 200 n_tokens: "2"
user_id=joe request at 23:39:19 response code: 200 n_tokens: "1"
user_id=joe request at 23:39:19 response code: 200 n_tokens: "0"
user_id=joe request at 23:39:19 response code: 429 n_tokens: {"detail":"Too Many Requests"}
user_id=joe request at 23:39:20 response code: 429 n_tokens: {"detail":"Too Many Requests"}
user_id=joe request at 23:39:27 response code: 200 n_tokens: "2"
user_id=joe request at 23:39:32 response code: 200 n_tokens: "3"
user_id=joe request at 23:39:33 response code: 200 n_tokens: "2"
user_id=joe request at 23:39:34 response code: 200 n_tokens: "1"
user_id=joe request at 23:39:35 response code: 200 n_tokens: "0"
user_id=joe request at 23:39:36 response code: 429 n_tokens: {"detail":"Too Many Requests"}
```

Stop the redis database and fastAPI servers:

```bash
redis-cli shutdown
rm dump.rdb
UVICORN_PID=$(pgrep -f "uvicorn host_api:app")
kill -15 $UVICORN_PID
rm nohup.out
```