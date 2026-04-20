# Covfee Starter Project

This repository is a minimal Covfee study with a folder-based runtime layout. The study entrypoint is `app.py`, development is configured from `covfee/dev/dev.env`, deployment is configured from `docker/.env`, and static project assets live in `www/`.

## Project layout

```text
covfee_project
├── app.py
├── www/
│   └── instructions.md
└── docker/
    ├── .env
    ├── Dockerfile
    ├── Dockerfile.local
    ├── docker-compose.yml
    ├── docker-compose.local.yml
    └── nginx.conf
```

## Development

Development is owned by the main `covfee` repository, not by this starter repo.

1. Clone/install the main `covfee` repository in editable mode.
2. From the `covfee` repo root, run:

```bash
# Edit dev/dev.env and set PROJECT_DIR=../covfee_project
scripts/dev-setup.sh
covfee-dev run
```

That starts four processes:

1. webpack dev server with hot reload
2. Flask backend with Python reload
3. Node Redux store service
4. standalone `www/` file server

## Environment files

- `covfee/dev/dev.env`: shared development settings used by `covfee-dev run`
- `docker/.env`: Docker Compose interpolation and runtime overrides for the deploy stack

Common variables:

- `COVFEE_HOST`: public backend hostname used in generated URLs
- `COVFEE_PORT`: public backend port used in generated URLs
- `COVFEE_PROJECT_WWW_URL`: public URL of the standalone `www` fileserver
- `COVFEE_REDUX_STORE_HOST`: hostname of the Node Redux store service
- `COVFEE_REDUX_STORE_PORT`: port of the Node Redux store service
- `COVFEE_DATABASE_PATH`: internal database path inside the deploy image/container
- `COVFEE_COVFEE_SECRET_KEY`: secret key for JWTs and signed links
- `COVFEE_ADMIN_USERNAME`: admin username
- `COVFEE_ADMIN_PASSWORD`: admin password

## Docker deployment

The default deploy image uses `docker/Dockerfile`, which clones `covfee` from GitHub at build time.

From the project root:

```bash
docker compose --env-file docker/.env -f docker/docker-compose.yml build
docker compose --env-file docker/.env -f docker/docker-compose.yml up
```

To stop all services:

```bash
docker compose --env-file docker/.env -f docker/docker-compose.yml down
```

The deploy stack starts three services:

1. `covfee`: the Flask/SocketIO backend
2. `store`: the standalone Node Redux store service from `covfee/store`
3. `www`: nginx serving the mounted `www/` folder

The backend image clones the remote `covfee` repository into `/opt/covfee`, installs it in editable mode, installs the Node dependencies for `covfee/shared`, `covfee/client`, and `store`, builds the production bundles, copies this project into `/opt/covfee-project`, and runs `covfee make . --deploy --no-launch` at build time using variables forwarded from `docker/.env`. At runtime the same `docker/.env` file is injected into the containers, and the only mounted host volume is `www/`, which is served by nginx.

### Building with a local `covfee` checkout

For local testing, `docker/Dockerfile.local` copies the sibling `covfee/` directory from the monorepo instead of cloning from GitHub. `docker/docker-compose.local.yml` overrides the default build config so `covfee` and `store` both build from that local checkout while `www` keeps using the same nginx service definition.

Run these commands from inside `covfee_project/`:

```bash
docker compose \
  --env-file docker/.env \
  -f docker/docker-compose.yml \
  -f docker/docker-compose.local.yml \
  build
```

Start all services:

```bash
docker compose \
  --env-file docker/.env \
  -f docker/docker-compose.yml \
  -f docker/docker-compose.local.yml \
  up
```

Stop all services:

```bash
docker compose \
  --env-file docker/.env \
  -f docker/docker-compose.yml \
  -f docker/docker-compose.local.yml \
  down
```

The local override changes the Docker build context to the monorepo root, so this layout expects `covfee_project/` and `covfee/` to be sibling directories. Docker will send everything under that root unless a top-level `.dockerignore` is added.
