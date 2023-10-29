.PHONY: all install mongo cassandra influx neo4j

PYTHON=python3
SCRIPTS_DIR=scripts

all:
	docker compose up -d

install:
	pip install -r scripts/requirements.txt

mongo:
	$(PYTHON) $(SCRIPTS_DIR)/mongo_script.py

cassandra:
	$(PYTHON) $(SCRIPTS_DIR)/cassandra_script.py

influx:
	$(PYTHON) $(SCRIPTS_DIR)/influx_script.py

neo4j:
	$(PYTHON) $(SCRIPTS_DIR)/neo4j_script.py

download:
	cd scripts && wget -O neo4j_financni_toky.csv https://data.brno.cz/datasets/mestobrno::finan%C4%8Dn%C3%AD-toky-neziskov%C3%A9mu-sektoru-v-%C4%8Dr-financial-subsidies-to-the-non-profit-sector-in-the-czech-republic.csv?where=1=1&outSR=%7B%22latestWkid%22%3A4326%2C%22wkid%22%3A4326%7D
	cd scripts && wget -O mongo_vyznamne_osobnosti.geojson https://data.brno.cz/datasets/mestobrno::hrobov%C3%A1-m%C3%ADsta-gravesites.geojson?where=1=1&outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D
	cd scripts && wget -O cassandra_kvalita_ovzdusi.geojson https://data.brno.cz/datasets/mestobrno::kvalita-ovzdu%C5%A1%C3%AD-air-quality.geojson?where=1=1&outSR=%7B%22wkid%22%3A4326%7D
	cd scripts && wget -O influx_dopavni_nehody.csv https://data.brno.cz/datasets/mestobrno::dopravn%C3%AD-nehody-traffic-accidents.csv?where=1=1&outSR=%7B%22latestWkid%22%3A5514%2C%22wkid%22%3A102067%7D 