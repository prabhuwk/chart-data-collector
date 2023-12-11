# Trading Bot
[![Build and Push Docker Image](https://github.com/prabhuwk/trading-bot/actions/workflows/main.yaml/badge.svg)](https://github.com/prabhuwk/trading-bot/actions/workflows/main.yaml)

![trading bot](design/trading_bot.png)

## Container Instances
![container instances](design/container_instances.png)

# For development

```bash
$ cat .env
DEBUG="True"
DHAN_CLIENT_ID="replace_client_id"
DHAN_ACCESS_TOKEN="replace_access_token"
$ docker-compose up --build
```
Click Run & Debug -> Select 'Python: Remote Attach'
