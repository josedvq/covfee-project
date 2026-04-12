# Covfee Starter Project

This repository is a minimal starting point for a Covfee study. It uses a Python project file, keeps local assets under `www/`, and supports both local testing and Docker-based deployment.

## Project layout

```text
covfee_project
├── getting_started.py
├── covfee.local.config.py
├── covfee.deployment.config.py
├── project_env.py
├── www/
│   └── instructions.md
└── docker/
    ├── Dockerfile
    ├── docker-compose.yml
    └── entrypoint.sh
```

## Local usage

1. Copy the environment template:

```bash
cp .env.example .env
```

2. Install Covfee so the `covfee` command is available. One option is:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install "git+https://github.com/josedvq/covfee.git"
```

3. Run the starter study from the project root:

```bash
covfee make getting_started.py
```

Covfee will initialize `.covfee/`, start the app, and open the admin panel at `http://localhost:5001/admin#` by default.

If you change the public host or port in `.env` for local testing, pass matching flags to `covfee make`, for example `covfee make getting_started.py --host my-host --port 5050`.

If you edit the study and want to rebuild the database, rerun:

```bash
covfee make getting_started.py --force
```

## Environment variables

The project config files read values from `.env`.

- `COVFEE_PROJECT_FILE`: Python study file to load.
- `COVFEE_HOST`: Public hostname used in generated URLs.
- `COVFEE_PUBLIC_PORT`: Public port used in generated URLs.
- `COVFEE_BIND_HOST`: Host that the deployment server binds to.
- `COVFEE_BIND_PORT`: Port that the deployment server binds to.
- `COVFEE_SECRET_KEY`: Secret key for JWTs and signed links.
- `COVFEE_ADMIN_USERNAME`: Admin username.
- `COVFEE_ADMIN_PASSWORD`: Admin password.
- `COVFEE_MEDIA_SERVER`: Whether Covfee should serve local media from `www/`.
- `COVFEE_MEDIA_URL`: External media base URL when `COVFEE_MEDIA_SERVER=false`.
- `COVFEE_SSL_CERT_FILE`: SSL certificate path relative to the project root or absolute.
- `COVFEE_SSL_KEY_FILE`: SSL key path relative to the project root or absolute.
- `COVFEE_PIP_SPEC`: Pip install target used by the Docker image.
- `COVFEE_FORCE_REBUILD`: Forces `covfee make --force` inside Docker on startup.

`covfee make` currently expects an explicit project file path, so local commands use `getting_started.py` directly instead of `covfee make .`.

## Docker deployment

Copy the env template first if you have not already:

```bash
cp .env.example .env
```

Then start the deployment stack from the project root:

```bash
docker compose --env-file .env -f docker/docker-compose.yml up --build
```

The container will:

1. install Covfee
2. initialize the database with `covfee make getting_started.py --no-launch --deploy`
3. start the server with `covfee start --deploy`

On later restarts it reuses the existing `.covfee/database.covfee.db` unless `COVFEE_FORCE_REBUILD=true`.

## SSL

To enable SSL, place your certificate and key inside the repository or use absolute paths, then set:

```bash
COVFEE_SSL_CERT_FILE=certs/fullchain.pem
COVFEE_SSL_KEY_FILE=certs/privkey.pem
```

When both values are set, Covfee switches its generated URLs to `https://`.
