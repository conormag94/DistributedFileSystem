docker-compose up -d
docker-compose run lock-service python manage.py recreate_db
docker-compose run directory-service python manage.py recreate_db
