# Django + Docker + Celery + AWS and Authentication Starter 

## Build Setup

```bash
# For Development Mode | serve at 8001 
$  docker-compose -f docker-compose.dev.yml up --build ld 
 
# For Production Mode serve at nginx listen 80 port
$ docker-compose -f docker-compose.prod.yml up --build -d
```

```bash
# Development environment variables file 
$ dev.env
 
# Production environment variables file 
$ prod.env
```

