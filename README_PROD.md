# Production Deploy

Secrets required in GitHub repository settings (Actions secrets):

- `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (or other registry credentials)
- `DEPLOY_HOST` (server IP)
- `DEPLOY_USER` (SSH user)
- `DEPLOY_SSH_KEY` (private key for SSH)
- `DEPLOY_PORT` (SSH port, default 22)

The workflow builds the Docker image, pushes to Docker Hub, then SSHs to the server and pulls/starts the updated `web` service and runs migrations and `collectstatic`.

On the server, prepare a deploy directory containing `docker-compose.prod.yml` and a `.env` with production values, then allow the workflow to `cd` into that directory (update path in workflow).
