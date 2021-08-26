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
	# python ./bin/merge_psms_files.py ./data/all_massive_search_psms.tsv ./data/all_massive_search_files.tsv ./data/merged_psms.tsv
	# python data/convert_tsv_to_sqlite.py database -out:peptide,scan ./data/merged_psms.tsv
	python ./bin/convert_tsv_to_sqlite.py database -out:peptide,scan ./data/merged_psms_small.tsv