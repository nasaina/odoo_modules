COMPOSE = docker compose
NAME = odoo

all: up

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) restart

clean:
	$(COMPOSE) down --rmi local --remove-orphans

fclean:
	$(COMPOSE) down -v --rmi all --remove-orphans

re: fclean up init

init:
	$(COMPOSE) run --rm web odoo -d odoo -i base --stop-after-init

.PHONY: all up down restart clean fclean re init
