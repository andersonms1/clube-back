SERVER_CONTAINER=club-back
FRONT_CONTAINER=club-front
MONGO_EXPRESS_COTAINER=club-express
EXEC=docker exec -it
attach:
	$(EXEC) $(SERVER_CONTAINER) bash
logs-back:
	docker logs -f $(SERVER_CONTAINER) 
logs-front:
	docker logs -f $(FRONT_CONTAINER) 
up-back:
	docker compose up back mongo redis -d
up-express:
	docker compose up mongo-express -d
test:
	$(EXEC) $(SERVER_CONTAINER) ./test.sh
