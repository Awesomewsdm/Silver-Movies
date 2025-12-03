# Silver Movies — Project Nexus (Presentation Outline)

Slide 1 — Title

- Title: Silver Movies — Project Nexus
- Subtitle: Movie recommendation API with TMDb integration
- Presenter: <Your Name>
- Speaker notes: Quick intro, what you'll cover (overview, ERD, endpoints, deployment).

Slide 2 — Overview

- Bullets:
  - Purpose: backend API to serve trending movies and personalized recommendations
  - Main features: JWT auth, favorites, Redis caching, TMDb integration
  - Audience: mentors reviewing architecture and API design
- Speaker notes: Emphasize learning goals and production-minded choices.

Slide 3 — Architecture Diagram (high level)

- Bullets:
  - Django REST API, PostgreSQL, Redis cache, Gunicorn + Docker
  - Optional: Celery for background tasks, Sentry for monitoring
- Speaker notes: Walk through request flow (user -> API -> TMDb/Cache -> DB).

Slide 4 — ERD (Data Model)

- Insert ERD image: `diagrams/silver_movies_erd.svg`
- Bullets:
  - Main entities: User, Movie, Genre, FavoriteMovie, Watchlist, TMDbCache
  - Relationships: User <-> FavoriteMovie (1:N), Movie <-> Genre (M:N via MovieGenre)
- Speaker notes: Explain why JSONB for metadata and denormalized fields on favorites.

Slide 5 — Data Model Rationale

- Bullets:
  - Use JSONB to store TMDb responses for flexible schema and quick snapshots
  - Denormalize small fields (title, tmdb_id) on FavoriteMovie for fast reads
  - Use unique constraints to prevent duplicates (user favorites, movie-genre)
- Speaker notes: Discuss trade-offs (storage vs read performance).

Slide 6 — Key Endpoints

- List:
  - `POST /api/auth/register/` — register and return JWT tokens
  - `POST /api/auth/token/` & `token/refresh/` — token management
  - `GET /api/movies/trending/` — TMDb trending (cached)
  - `GET /api/movies/{tmdb_id}/recommendations/` — TMDb recommendations
  - `GET/POST /api/favorites/`, `DELETE /api/favorites/{id}/` — manage favorites
- Speaker notes: Mention auth requirement and typical response shapes.

Slide 7 — Authentication & Security

- Bullets:
  - JWT with short-lived access tokens and refresh tokens
  - Use HTTPS in production; store secrets in environment variables
  - TokenBlacklist model optional for revocation
- Speaker notes: Explain reason for refresh tokens and blacklist trade-offs.

Slide 8 — Performance & Caching

- Bullets:
  - Redis used for caching TMDb responses (trending/results) with TTL
  - Cache fallback: serve stale cached response on TMDb failures (configurable)
  - Index important columns (tmdb_id, foreign keys) and use JSONB GIN index if querying metadata
- Speaker notes: Quick benchmark idea and cache invalidation strategy.

Slide 9 — Testing & CI

- Bullets:
  - Unit tests for TMDb client and API views
  - GitHub Actions workflow runs tests and builds image
  - Postman collection included for manual smoke tests
- Speaker notes: Mention adding coverage reporting later.

Slide 10 — Deployment

- Bullets:
  - Dockerized app with `Dockerfile` and `docker-compose.yml`
  - Render manifest included (`render.yaml`) — release command runs migrations & collectstatic
  - Environment variables: `DATABASE_URL`, `TMDB_API_KEY`, `REDIS_URL`, secret key
- Speaker notes: Suggest health checks and restart strategies on the host.

Slide 11 — Demos & Postman

- Bullets:
  - Show Postman collection at `postman/silver-movies.postman_collection.json`
  - Demo flows: register -> get token -> create favorite -> list favorites
- Speaker notes: Explain variables `base_url` and token capture scripts.

Slide 12 — Next Steps

- Bullets:
  - Add Celery for scheduled cache warmups
  - Add Sentry and structured logging
  - Expand test coverage and add E2E tests for deployed service
- Speaker notes: Mention potential features like user profiles and recommendations tuning.

Slide 13 — Q&A / Links

- Bullets:
  - Repo: GitHub link
  - Postman collection: repo path
  - ERD image: `diagrams/silver_movies_erd.svg`
- Speaker notes: Invite questions and feedback.
