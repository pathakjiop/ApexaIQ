## Overview
Essential Docker commands for container management, categorized by functionality for easy reference.

## Container Management

### Lifecycle Commands

```bash
# Run a container
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]

# Examples:
docker run nginx                          # Run nginx container
docker run -d nginx                       # Run in detached mode
docker run -p 8080:80 nginx              # Port mapping
docker run -v /host/path:/container/path nginx  # Volume mount

# Start/Stop containers
docker start <container>                  # Start stopped container
docker stop <container>                   # Stop running container
docker restart <container>                # Restart container
docker pause <container>                  # Pause container
docker unpause <container>                # Unpause container

# Remove containers
docker rm <container>                     # Remove stopped container
docker rm -f <container>                  # Force remove running container
```


### Container Information

```bash
# List containers
docker ps                                # Running containers
docker ps -a                             # All containers
docker ps -q                             # Only container IDs

# Container details
docker logs <container>                  # View logs
docker logs -f <container>               # Follow logs
docker inspect <container>               # Detailed information
docker stats <container>                 # Resource usage
docker top <container>                   # Running processes

# Execute commands
docker exec [OPTIONS] <container> <command>
docker exec -it <container> bash         # Interactive shell
docker exec <container> ls -la           # Run command
```

## Image Management

### Working with Images


```bash
# Pull images
docker pull <image:tag>                  # Download image

# List images
docker images                            # Local images
docker images -a                         # All images

# Remove images
docker rmi <image>                       # Remove image
docker rmi $(docker images -q)           # Remove all images

# Build images
docker build [OPTIONS] PATH              # Build from Dockerfile
docker build -t myapp:latest .          # Tag during build

# Save/Load images
docker save -o image.tar <image>         # Save image to tar
docker load -i image.tar                # Load image from tar
```

## Dockerfile Basics

### Common Instructions

```dockerfile
FROM ubuntu:20.04                        # Base image
LABEL maintainer="name@email.com"        # Metadata
WORKDIR /app                             # Working directory
COPY . .                                 # Copy files
RUN apt-get update && apt-get install -y python3  # Run commands
EXPOSE 80                                # Expose port
CMD ["python3", "app.py"]               # Default command
```

## Networking

### Network Commands

```bash
# List networks
docker network ls

# Create network
docker network create my-network

# Connect container to network
docker network connect my-network <container>

# Inspect network
docker network inspect my-network
```

### Common Network Examples
```bash
# Create and use custom network
docker network create myapp-network
docker run -d --name web --network myapp-network nginx
docker run -it --network myapp-network alpine ping web
```

## Volumes and Storage

### Volume Management

```bash
# List volumes
docker volume ls

# Create volume
docker volume create my-volume

# Use volume
docker run -v my-volume:/data nginx

# Inspect volume
docker volume inspect my-volume

# Remove volume
docker volume rm my-volume
```

### Bind Mounts

```bash
# Bind mount host directory
docker run -v /host/path:/container/path nginx

# Read-only bind mount
docker run -v /host/path:/container/path:ro nginx
```

## Docker Compose Basics

### Common Compose Commands
```bash
# Start services
docker-compose up                        # Start all services
docker-compose up -d                     # Start in background
docker-compose up service1              # Start specific service

# Stop services
docker-compose down                      # Stop and remove
docker-compose stop                     # Stop only

# View logs
docker-compose logs                     # All services
docker-compose logs service1            # Specific service

# Manage services
docker-compose ps                       # Service status
docker-compose exec service1 bash       # Execute command
```

### Sample docker-compose.yml

```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
  database:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
```

## Useful Tips and Shortcuts

### Common Patterns

```bash
# Clean up unused resources
docker system prune                      # Remove unused data
docker container prune                  # Remove stopped containers
docker image prune                      # Remove unused images

# One-liner for cleanup
docker system prune -a -f               # Force remove all unused

# Run and auto-remove
docker run --rm -it ubuntu bash         # Auto remove after exit

# Copy files
docker cp file.txt <container>:/path/   # Host to container
docker cp <container>:/path/file.txt .  # Container to host
```

### Development Workflow

```bash
# Development with bind mounts for live reload
docker run -v $(pwd):/app -p 3000:3000 node-app

# Build and run with tags
docker build -t myapp:dev .
docker run -p 8080:80 myapp:dev

# Debugging containers
docker exec -it <container> sh          # Shell access
docker logs --tail 50 -f <container>    # Follow last 50 lines
```

## Common Use Cases

### Web Application

```bash
docker run -d --name web -p 80:80 -v ./site:/usr/share/nginx/html nginx
```

### Database with Persistence

```bash
docker run -d --name db -p 5432:5432 \
  -v db_data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=mypassword postgres
```

### Development Environment

```bash
docker run -it --rm -v $(pwd):/workspace -w /workspace node:14 bash
```
