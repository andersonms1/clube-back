SERVER_CONTAINER=club-back
MONGO_EXPRESS_COTAINER=club-express
EXEC=docker exec -it
attach:
	$(EXEC) $(SERVER_CONTAINER) bash
logs-back:
	docker logs -f $(SERVER_CONTAINER) 
up-back:
	docker compose up back mongo redis -d
up-express:
	docker compose up mongo-express -d