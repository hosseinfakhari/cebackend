# Calculation Engine Backend.
    

## first build docker image to run the application easily:
```shell
make build-docker
```

or if you are using windows and suffer from windows command line:
```
docker build -t cebackend . --no-cache
```

### create `.env` file and fill it like the example env file
```shell
cp .env.example .env
```

### then run the docker compose to setup the database and apply migration:
```shell
docker compose up -d
docker compose exec backend python manage.py migrate
```

### and ofcourse create a super user to access the admin panel:
```shell
docker compose exec backend python manage.py createsuperuser
```



## To analyze any activity data you need to have the `co2e factors` data in database first. you can load the factor data by `admin panel` or management command:

```shell
docker compose exec backend python manage.py load_factors uploads/CSV-Emission-Factors-and-Activity-Data-Emission-Factors.csv --replace
```

### finally locate to http://localhost:8000 to access the app frontend
upload any activity data fist and then get the result by clicking on `get emission data` button