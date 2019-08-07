rm -rf index/migrations
docker rm -f scoreboard postgresql nginx
docker-compose up -d postgresql
sleep 2
docker-compose up -d scoreboard
sleep 3
docker exec -i postgresql psql scoreboard < postgresql/user.sql
docker exec -i scoreboard python3 manage.py collectstatic
docker-compose up -d nginx
# chown www-data:www-data .