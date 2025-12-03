Silver Movies — Deployment Guide

This document explains how to deploy the Silver Movies backend to a production host (Render), what environment variables are required, health checks, and how to validate the deployment.

1. Recommended runtime

- Use the Docker image (the repo includes a `Dockerfile`). Render's Docker environment is recommended to guarantee parity with local builds.

2. Required environment variables

- `DJANGO_SECRET_KEY` (string) — strong random value, keep secret.
- `DJANGO_DEBUG` (boolean) — set to `False` in production.
- `DATABASE_URL` (string) — Postgres connection URL (Render Postgres will provide this when you provision a DB).
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` — optional local/dev helpers; prefer `DATABASE_URL` in production.
- `TMDB_API_KEY` — your TMDb API key.
- `ALLOWED_HOSTS` — comma-separated hostnames (e.g., `silver-movies.onrender.com`).
- Optional: `SENTRY_DSN` — if you integrate Sentry for error tracking.

3. Render setup (Docker)

- In Render dashboard: New → Web Service → Connect GitHub repo → Branch `main`.
- Environment: `Docker`.
- Root Directory: leave blank (uses repo root) unless you have a monorepo.
- Dockerfile path: `Dockerfile` (repo root).
- Start command: use the Docker CMD (defaults to Gunicorn in the Dockerfile).
- Release Command (recommended):

  ```bash
  python project_nexus/manage.py migrate --noinput && python project_nexus/manage.py collectstatic --noinput
  ```

- Health check path: `/api/health/` (HTTP 200 expected).
- Add environment variables listed in section (2) in the Render service Environment tab (do not store secrets in the repository).
- Provision a Render Postgres DB (optional) — attach it to the service; Render will add `DATABASE_URL` automatically.

4. Dockerfile notes

- The Dockerfile sets the working directory to `/app/project_nexus` and runs Gunicorn.
- Ensure `requirements.txt` contains `gunicorn` and production dependencies (`whitenoise`, `dj-database-url`).

5. Verifying the deployment

- Health: `curl -i https://<your-service>.onrender.com/api/health/` → should return 200 and JSON `{"status":"ok"}`.
- Swagger: `https://<your-service>.onrender.com/api/docs/` can be used to inspect endpoints.
- Smoke tests:
  - Register: `POST /api/auth/register/` (username, email, password) → returns `access` and `refresh` tokens.
  - Token: `POST /api/auth/token/` with username/password → returns tokens.
  - Trending: `GET /api/movies/trending/` (public endpoint) → returns TMDb trending movies.
  - Favorites: `GET/POST /api/favorites/` (requires Bearer token).

6. Post-deploy operations

- Running migrations: the Release Command runs migrations, but you can run them manually from the service shell if needed.
- Logs: Use Render logs to inspect startup errors and release output.

7. Security and monitoring

- Set `DJANGO_DEBUG=False` and keep `DJANGO_SECRET_KEY` secret.
- Set proper `ALLOWED_HOSTS` and configure CORS if you have a frontend on a different domain.
- Integrate Sentry or another error tracker; set `SENTRY_DSN` in Render env.

8. Rollback and backups

- Use Render's deploy history to rollback to a previous image.
- For DB backups, enable automatic backups in Render Postgres or configure scheduled exports.

9. Troubleshooting

- If deploy shows `Exited with status 128`, inspect logs for failing release commands or git/submodule errors.
- If Gunicorn can't find `project_nexus.wsgi`, ensure the Docker `WORKDIR` is `/app/project_nexus` and the image was rebuilt.

Endpoints Overview

- `GET /api/health/` — health check (public)
- `POST /api/auth/register/` — register user, returns JWT tokens
- `POST /api/auth/token/` — obtain JWT tokens
- `POST /api/auth/token/refresh/` — refresh access token
- `GET /api/auth/me/` — get current user (requires auth)
- `GET /api/movies/trending/` — get TMDb trending movies
- `GET /api/movies/<tmdb_id>/recommendations/` — movie recommendations via TMDb
- `GET /api/favorites/` — list favorites for current user (requires auth)
- `POST /api/favorites/` — create favorite (requires auth)
- `DELETE /api/favorites/<id>/` — remove favorite (requires auth)

If you want, I can:

- Add this `README_DEPLOY.md` to the repo (already added).
- Generate a short `DEPLOYMENT_CHECKLIST.md` for reviewers.
- Create a Postman collection and include it in the repo for reviewers.

Which of these should I do next?
