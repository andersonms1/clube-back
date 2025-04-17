SERVER_CONTAINER=club-back
EXEC=docker exec -it
attach:
	$(EXEC) $(SERVER_CONTAINER) bash
logs-back:
	docker logs -f $(SERVER_CONTAINER) 
up-back:
	docker compose up back mongo redis -d