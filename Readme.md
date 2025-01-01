# Simple e-commerce backend service using microservices 
A learning-focused implementation of a microservices-based e-commerce backend system. This project demonstrates microservices architecture, message queuing, and containerization principles using modern Python technologies.

## Technology Stack

#### Backend Framework & Tools

FastAPI: Modern, fast web framework for building APIs
SQLAlchemy: SQL toolkit and ORM
Alembic: Database migration tool
Pydantic: Data validation using Python type annotations

#### Data Storage & Messaging

PostgreSQL: Primary database for all services
RabbitMQ: Message broker for inter-service communication

#### Infrastructure

Docker: Containerization of services
Docker Compose: Multi-container orchestration

###Project Structure
```
├── main_service/             # User and Product management service
│   ├── alembic/              # Database migrations
│   ├── messaging/            # RabbitMQ communication handlers
│   ├── user/                 # User module
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── crud.py          # Database operations
│   ├── product/             # Product module
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── crud.py
│   ├── core/                # Core configurations
│   │   ├── db.py           # Database configuration
│   │   └── config.py       # Service configuration
│   ├── Dockerfile
│   ├── main.py             # FastAPI application entry point
│   ├── requirements.txt
│   └── .env
│
├── order_service/           # Order management service
│   ├── alembic/
│   ├── messaging/
│   ├── order/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── crud.py
│   ├── core/
│   │   ├── db.py
│   │   └── config.py
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── docker-compose.yml       # Service orchestration configuration
├── Makefile                # Development automation commands
└── README.md
```

### API Documentation
Once the services are running, access the API documentation:

Main Service: http://localhost:8000/docs

Order Service: http://localhost:8001/docs


#### Note
This project is intended for learning purposes and demonstrates microservices architecture concepts. It may not be suitable for production use without additional security and performance considerations.