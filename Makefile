.PHONY: all install mongo cassandra influx neo4j

PYTHON=python3
SCRIPTS_DIR=scripts

all:
	docker compose up -d

install:
	pip install -r scripts/requirements.txt

mongo:
	$(PYTHON) $(SCRIPTS_DIR)/mongo.py

cassandra:
	$(PYTHON) $(SCRIPTS_DIR)/cassandra_script.py

influx:
	$(PYTHON) $(SCRIPTS_DIR)/influx.py

neo4j:
	$(PYTHON) $(SCRIPTS_DIR)/neo4j.py