To install requirements use: pip install -r requirements.txt

To run containers : docker-compose up -d


# Backup
docker exec CONTAINER /usr/bin/mysqldump -u root --password=root DATABASE > backup.sql

# Restore
cat backup.sql | docker exec -i CONTAINER /usr/bin/mysql -u root --password=root DATABASE#   E - c o m m e r c e  
 