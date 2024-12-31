# Simple e-commerce backend service using microservices architecture. 
*(for learning purposes)*

### Technologies used:
- FastAPI
- SQLAlchemy
- Alembic
- Docker
- RabbitMQ
- PostgreSQL
- Pydantic

### Folder structure:
```
main_service/
|   alembic/
|   user/
        models.py
        schemas.py
        crud.py
|   product/
        models.py
        schemas.py
        crud.py
|   core/
        db.py
        config.py
│   Dockerfile (Main service Dockerfile)
│   main.py (FastAPI entrypoint for main service)
│   requirements.txt (Main service requirements)
|   .env (Environment variables)
order_service/
|   alembic/
|   order/
        models.py
        schemas.py
        crud.py
|   core/
|       db.py
        config.py
│   Dockerfile (Order service Dockerfile)
│   main.py (FastAPI entrypoint for order service)
│   requirements.txt (Order service requirements)
|   .env (Environment variables)
docker-compose.yml (Docker compose file)
Makefile (commands for running the services)
README.md
```

Main service is responsible for handling users and products. 
Tables created in the database are:
- User
- Product

Order service is responsible for handling orders.
Tables created in the database are:
- Order


Database used is PostgreSQL.
Message broker used is RabbitMQ.