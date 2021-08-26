#Docker Compose
server-compose-interactive:
	docker-compose build
	docker-compose up 

server-compose-background:
	docker-compose build
	docker-compose up -d 

attach:
	docker exec -i -t gnps_datasetcache_gnps-datasetcache-web_1 /bin/bash

attach-worker:
	docker exec -i -t gnps_datasetcache_gnps-datasetcache-worker_1  /bin/bash

create_db:
	# echo -e "scan\tpeptide\tcharge\tfileidx" | cat all_massive_search_psms.tsv > all_massive_search_psms_with_headers.tsv
	python data/convert_tsv_to_sqlite.py database -out:peptide,scan,peptide+scan data/all_massive_search_psms_with_headers.tsv