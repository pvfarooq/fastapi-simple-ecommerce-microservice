
.PHONY: help
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-25s\033[0m %s\n", $$1, $$2}'


.PHONY: main-sh
main-sh: ## Run bash shell in main service container
	docker compose exec main_app /bin/bash

.PHONY: order-sh
order-sh: ## Run bash shell in order service container
	docker compose exec order_app /bin/bash

.PHONY: product-sh
product-sh: ## Run bash shell in product service container
	docker compose exec product_app /bin/sh

.PHONY: main-alembic-rev
main-alembic-rev: ## Create alembic revision in main service container
	@echo "Enter revision message:"; \
	read message && \
	if [ -z "$$message" ]; then \
		echo "Revision message cannot be empty"; \
		exit 1; \
	fi; \
	docker compose exec main_app alembic revision --autogenerate -m "$$message"

.PHONY: order-alembic-rev
order-alembic-rev: ## Create alembic revision in order service container
	@echo "Enter revision message:"; \
	read message && \
	if [ -z "$$message" ]; then \
		echo "Revision message cannot be empty"; \
		exit 1; \
	fi; \
	docker compose exec order_app alembic revision --autogenerate -m "$$message"

.PHONY: main-alembic-up
main-alembic-up: ## Alembic upgrade head in main service
	docker compose exec main_app alembic upgrade head

.PHONY: order-alembic-up
order-alembic-up: ## Alembic upgrade head in order service
	docker compose exec order_app alembic upgrade head

.PHONY: main_alembic_down
main_alembic_down: ## Alembic downgrade head in main service
	docker compose exec main_app alembic downgrade -1

.PHONY: order_alembic_down
order_alembic_down: ## Alembic downgrade head in order service
	docker compose exec order_app alembic downgrade -1
