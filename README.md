# Calculation Engine Backend.
    

docker build -t cebackend . --no-cache

docker compose exec backend python manage.py migrate

docker compose exec backend python manage.py load_factors uploads/CSV-Emission-Factors-and-Activity-Data-Emission-Factors.csv --replace