.PHONY: all install mongo cassandra influx neo4j

PYTHON=python3
SCRIPTS_DIR=scripts

all:
	docker compose up -d

install:
	pip install -r scripts/requirements.txt

mongo:
	$(PYTHON) $(SCRIPTS)/mongo.py

cassandra:
	$(PYTHON) $(SCRIPTS)/cassandra.py

influx:
	$(PYTHON) $(SCRIPTS)/influx.py

neo4j:
	$(PYTHON) $(SCRIPTS)/neo4j.py