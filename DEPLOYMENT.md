\# Production Deployment Guide



\## Prerequisites



\- Docker 20.10+

\- Docker Compose 1.29+

\- 8GB+ RAM

\- 20GB+ Storage



\## Quick Start



\### 1. Build and Start Services

```bash

docker-compose up -d

```



\### 2. Verify Services

```bash

docker-compose ps

```



Expected output:

\- `mena-api` - Running on port 8000

\- `mena-dashboard` - Running on port 8501

\- `mena-mlflow` - Running on port 5000

\- `mena-nginx` - Running on ports 80/443



\### 3. Access Services



\- \*\*API\*\*: http://localhost:8000/docs

\- \*\*Dashboard\*\*: http://localhost:8501

\- \*\*MLflow\*\*: http://localhost:5000



\## Configuration



\### Environment Variables



Edit `docker-compose.yml` to customize:

```yaml

environment:

&nbsp; - MODEL\_DEVICE=cuda  # Change to 'cuda' for GPU

&nbsp; - LOG\_LEVEL=DEBUG    # DEBUG, INFO, WARNING, ERROR

&nbsp; - BATCH\_SIZE=32      # Adjust based on memory

```



\### SSL/TLS (Production)



1\. Generate certificates:

```bash

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \\

&nbsp; -keyout nginx/ssl/key.pem \\

&nbsp; -out nginx/ssl/cert.pem

```



2\. Update `nginx.conf` with SSL configuration



\## Monitoring



\### View Logs

```bash

\# All services

docker-compose logs -f



\# Specific service

docker-compose logs -f api

```



\### Health Checks

```bash

curl http://localhost:8000/health

```



\## Scaling



\### Horizontal Scaling

```bash

docker-compose up -d --scale api=3

```



\### Resource Limits



Edit `docker-compose.yml`:

```yaml

services:

&nbsp; api:

&nbsp;   deploy:

&nbsp;     resources:

&nbsp;       limits:

&nbsp;         cpus: '2'

&nbsp;         memory: 4G

```



\## Backup



\### Data Volumes

```bash

\# Backup

docker run --rm -v mena\_mlruns:/data -v $(pwd):/backup \\

&nbsp; alpine tar czf /backup/mlruns-backup.tar.gz /data



\# Restore

docker run --rm -v mena\_mlruns:/data -v $(pwd):/backup \\

&nbsp; alpine tar xzf /backup/mlruns-backup.tar.gz -C /

```



\## Troubleshooting



\### Container Won't Start

```bash

docker-compose logs api

docker-compose restart api

```



\### Out of Memory



Increase Docker resources or reduce batch size



\### Port Conflicts



Change ports in `docker-compose.yml`



\## Security



\- Change default ports

\- Enable SSL/TLS

\- Use secrets management

\- Implement authentication

\- Regular updates



\## Kubernetes Deployment



See `k8s/` directory for Kubernetes manifests.



\## Support



For issues, check logs or contact support.

