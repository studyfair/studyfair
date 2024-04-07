# Abstract

The project is intended to build reliable and extendable platform for automatic code clone detection. While the primary
use-cases is considered to be student homework cheating detection, it can be used to automate clone detection of any programs.

## Installation

### Prerequisites

The instructions below were on tested on Ubuntu 22.04 with the following packages installed:

- Docker Engine (Community) 26.0.0 with compose plugin (2.25.0)

Make sure you have docker installed, other versions are highly likely to work too.

### Prepare docker images

1. Clone this git repository:

   ```shell
   git clone https://github.com/viralpraxis/spbu-anticheat-project.git
   ```

2. Enter the repository and build docker images:

   ```shell
   cd spbu-anticheat-project && docker compose build --pull
   ```

3. Although the system is built with intention of begin language-agnostic, currently each language (ATM only python) requires it own engine. To build the python engine, one should execute

   ```shell
   docker build -t python-mutator:latest mutator
   ```

### Fill in credentials

Now you should configure credentials for each service.

   Start with creating VCS-ignored dotenv files:

   ```shell
   cp .env.sample .env
   cp .postgresql.env.sample .postgresql.env
   cp .s3.env.sample .s3.env
   ```

   Open `.env` and fill in the following variables:

   1) set `S3_ACCESS_KEY_ID` via `openssl rand -hex 8`;
   2) set `S3_SECRET_ACCESS_KEY` via `openssl rand -hex 8`;
   3) set `DETECTOR_ACCESS_TOKEN` via `openssl rand -hex 16`;
   4) set `DETECTOR_WEBHOOK_ACCESS_TOKEN` via `openssl rand -hex 16`;
   5) set `SECRET_KEY_BASE` via `openssl rand -hex 64`;
   6) if your are going to use Telegram Bot integration, set `TELEGRAM_BOT_API_TOKEN` to the corresponding value.

2. (optional) Change Minio root user credentials in `.s3.env`.

3. (optional) Change PostgreSQL DSN options in `.postgresql.env`. Make sure it's aligned with `.env` `POSTGRES_*` variables.

### Prepare SSL certificates

Generate certificates by running

```shell
openssl req -newkey rsa:2048 -sha256 -nodes -x509 -days 365 \
  -keyout ca.key \
  -out ca.crt \
  -subj "/C=RU/ST=Saint-Petersburg/L=Saint-Petersburg/O=Example Inc/CN=<IP-ADDRESS>" \
  && mv ca.{key,crt} nginx/ssl
```

don't forget to replace `<IP-ADDRESS>` with your public IP address or `localhost`.

### Runtime configuration

1. Run `docker compose up -d`. Wait a few seconds and make sure all is working as expected via `docker compose ps -a`.

2. (hopefully I'l make this step at least semi-automatic)

   To configure Minio buckets, visit http://localhost:9001/login, login via username & password mentioned in `.s3.env` and create a bucket named `production`. Change it's visibility (aka "access policy" to `public`.

   Now open "access keys" -> "created access key" and fill in the form with the values from `S3_ACCESS_KEY_ID` and `S3_SECRET_ACCESS_KEY`.


3. (optional) If your are going to use Telegram Bot integration, you should have public IP address available. If you don't have one, you might use
[ngrok](https://github.com/inconshreveable/ngrok), [CF tunnel](https://www.cloudflare.com/products/tunnel/) or any other similar tool. For example, if you're using `ngrok` simply run `ngrok http https://localhost:443`. You should set webhook URL via

   ```bash
   docker compose exec frontier-web bundle exec rake telegram:bot:set_webhook[https://your-public-ip-address]
   ```

   NOTE: enlightened zsh users will have to escape `[` and `]`:


   ```bash
   docker compose exec frontier-web bundle exec rake telegram:bot:set_webhook\[https://your-public-ip-address\]
   ```

### Make sure everything in working

You'll need to created a user to log in. Run the following command:

```shell
docker compose exec frontier-web bundle exec rails db:seed
```

Visit https://localhost/admin and login via credentials mentioned in `frontier/db/seeds.rb`.

## API

Currenly there are ways of interacting with the system: web UI and RESTful HTTP API.

### HTTP API

[TODO]
