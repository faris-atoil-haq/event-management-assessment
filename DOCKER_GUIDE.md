# Docker Commands for Event Management System

## Prerequisites
Make sure you have Docker and Docker Compose installed:
- [Install Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Quick Start

### Development Environment
```bash
# Build and start development environment
docker-compose -f docker-compose.dev.yml up --build

# Run in background
docker-compose -f docker-compose.dev.yml up -d --build

# View logs
docker-compose -f docker-compose.dev.yml logs -f web

# Stop services
docker-compose -f docker-compose.dev.yml down
```

### Production Environment
```bash
# Build and start production environment
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

## Useful Commands

### Database Operations
```bash
# Run Django migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell

# Load fixture data
docker-compose exec web python manage.py loaddata fixtures/initial_data.json
```

### Container Management
```bash
# View running containers
docker-compose ps

# Access container shell
docker-compose exec web bash
docker-compose exec db psql -U postgres -d event_management_db

# View container logs
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Restart specific service
docker-compose restart web
docker-compose restart db
```

### Build and Cleanup
```bash
# Rebuild containers
docker-compose build --no-cache

# Remove containers and volumes
docker-compose down -v

# Remove all containers, networks, and images
docker-compose down --rmi all -v --remove-orphans

# Clean up Docker system
docker system prune -a
```

### Database Backup and Restore
```bash
# Backup database
docker-compose exec db pg_dump -U postgres event_management_db > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres event_management_db < backup.sql

# Access database directly
docker-compose exec db psql -U postgres -d event_management_db
```

### Static Files and Media
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# View static files volume
docker volume inspect event-management-assessment_static_volume
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Django settings
DEBUG=0
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database
DATABASE_URL=postgresql://postgres:postgres123@db:5432/event_management_db

# Redis (optional)
REDIS_URL=redis://redis:6379/1

# Email settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (optional, for production file storage)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

## Services Overview

### Web Application (Django)
- **Port:** 8000
- **URL:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/doc/

### Database (PostgreSQL)
- **Port:** 5432
- **Database:** event_management_db
- **User:** postgres
- **Password:** postgres123

### Cache (Redis)
- **Port:** 6379
- **Database:** 1

### Reverse Proxy (Nginx)
- **Port:** 80 (HTTP), 443 (HTTPS)
- **Features:** Load balancing, static file serving, rate limiting

## Monitoring and Health Checks

### Health Check Endpoints
```bash
# Application health
curl http://localhost:8000/health/

# Nginx health
curl http://localhost/health/

# Database connection test
docker-compose exec web python manage.py check --database default
```

### Performance Monitoring
```bash
# View resource usage
docker stats

# Monitor specific service
docker stats event-management-assessment_web_1

# View disk usage
docker system df
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Check what's using the port
   netstat -tulpn | grep :8000
   
   # Kill the process or change port in docker-compose.yml
   ```

2. **Database connection error:**
   ```bash
   # Check if database is running
   docker-compose ps db
   
   # View database logs
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

3. **Static files not loading:**
   ```bash
   # Collect static files
   docker-compose exec web python manage.py collectstatic --noinput
   
   # Check nginx configuration
   docker-compose exec nginx nginx -t
   ```

4. **Permission denied errors:**
   ```bash
   # Fix file permissions
   docker-compose exec web chown -R appuser:appuser /app
   ```

### Debugging
```bash
# Enable debug mode
docker-compose -f docker-compose.dev.yml up

# View detailed logs
docker-compose logs --tail=100 -f web

# Access container for debugging
docker-compose exec web bash
```

## Production Deployment

### SSL Configuration
1. Obtain SSL certificates (Let's Encrypt recommended)
2. Place certificates in `ssl/` directory
3. Uncomment HTTPS server block in `nginx.conf`
4. Update environment variables

### Security Checklist
- [ ] Change default passwords
- [ ] Set strong SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Enable HTTPS
- [ ] Set up proper firewall rules
- [ ] Configure backup strategy
- [ ] Set up monitoring and logging

### Scaling
```bash
# Scale web service
docker-compose up --scale web=3

# Use load balancer
# Update nginx.conf upstream block with multiple servers
```