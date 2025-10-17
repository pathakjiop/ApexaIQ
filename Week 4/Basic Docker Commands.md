# Docker Basics for Beginners

## What is Docker?
Docker helps you run applications in isolated containers. Think of containers as lightweight virtual machines.

## Basic Commands You'll Use Daily

### Starting and Stopping Containers
```bash
# Download and run a container
docker run nginx

# Run in background (detached mode)
docker run -d nginx

# Stop a container
docker stop container_name

# Start a stopped container
docker start container_name

# Restart a container
docker restart container_name
```

### Viewing Containers
```bash
# See running containers
docker ps

# See all containers (running and stopped)
docker ps -a

# View container logs
docker logs container_name

# See real-time logs
docker logs -f container_name
```

### Removing Containers
```bash
# Remove a stopped container
docker rm container_name

# Remove a running container
docker rm -f container_name
```

## Working with Images

### Getting Images
```bash
# Download an image
docker pull nginx

# See downloaded images
docker images
```

### Building Your Own Images

Create a file called `Dockerfile`:
```dockerfile
FROM nginx
COPY . /usr/share/nginx/html
```

Then build it:
```bash
docker build -t my-website .
```

## Common Examples for Beginners

### Run a Website
```bash
docker run -d -p 80:80 --name my-website nginx
```
- `-d` = run in background
- `-p 80:80` = connect computer's port 80 to container's port 80
- `--name my-website` = give container a friendly name

### Run with Your Files
```bash
docker run -d -p 80:80 -v $(pwd):/usr/share/nginx/html nginx
```
- `-v $(pwd):/path` = use your current folder in the container

### Run a Database
```bash
docker run -d --name my-db -e POSTGRES_PASSWORD=mysecretpassword postgres
```
- `-e` = set environment variable (like password)

## Useful Tips

### Cleaning Up
```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune
```

### Getting Inside a Container
```bash
# Open terminal inside running container
docker exec -it container_name bash
```

### Copy Files
```bash
# Copy from computer to container
docker cp file.txt container_name:/path/

# Copy from container to computer
docker cp container_name:/path/file.txt .
```

## Simple docker-compose.yml (Multiple Containers)

Create `docker-compose.yml`:
```yaml
version: '3'
services:
  website:
    image: nginx
    ports:
      - "80:80"
  database:
    image: postgres
    environment:
      POSTGRES_PASSWORD: mypassword
```

Then run:
```bash
docker-compose up -d    # Start all services
docker-compose down     # Stop all services
```

## Common Mistakes to Avoid

1. **Don't forget `-d`** for background containers
2. **Use `--name`** to give containers friendly names
3. **Remember port mapping** (`-p host:container`)
4. **Save important data** with volumes or your computer won't lose it

## Quick Reference

| Command | What it does |
|---------|--------------|
| `docker run nginx` | Start nginx container |
| `docker ps` | See running containers |
| `docker stop name` | Stop a container |
| `docker logs name` | See container output |
| `docker exec -it name bash` | Get inside container |
| `docker-compose up -d` | Start multiple services |

Start with these basics! Once you're comfortable, you can explore more advanced features.