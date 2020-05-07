# airflow-docker

This is yet another Airflow setup example, aiming to offer an easy to start and decent **DAGs development environment**, reduce the friction for new comers and serve as entry point for those who are familiar with docker/docker-compose and is curious about Airflow (or is just tired of setting things up).


The only requirement is to have a up-to-date [docker-compose installation](https://docs.docker.com/compose/install/).

**Here we use the [official docker images](https://hub.docker.com/r/apache/airflow) provided by Apache Airflow starting from version [1.10.10](https://airflow.apache.org/blog/airflow-1.10.10/#add-production-docker-image-support)**

> **NOTE:** Once you finished the setup, airflow will start with your system _(check docker-compose.yaml for `restart: always`)_, so **be mindful about the DAGs you leave 'on'**. My suggestion is to always leave them **off** and enable back as needed.


From now on I am assuming you are in a directory containing a **`docker-compose.yaml`**. I suggest to clone this repo and open the terminal in the directory.

## Setup

### Step 1: Create the `.env` file

This file contains the Airflow configuration as environment variables.

```
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@postgres:5432/airflow
AIRFLOW__CORE__FERNET_KEY=-z10C-HjsdiHJDqq98gzTye-1LES4Kfz3UVouMp6OrA=
AIRFLOW__CORE__LOAD_EXAMPLES=False
AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags
AIRFLOW__CORE__EXECUTOR=CeleryExecutor
AIRFLOW__CELERY__BROKER_URL=redis://:REDIS_PASSWORD@redis:6379/1
AIRFLOW__CELERY__RESULT_BACKEND=db+postgresql://airflow:airflow@postgres:5432/airflow
AIRFLOW_CONN_POSTGRES_DEFAULT=postgresql://airflow:airflow@postgres:5432/airflow
AIRFLOW__WEBSERVER__EXPOSE_CONFIG=true
```

For making things straightforward I just copied over the contents of my `.env`, but as you know is always good to keep things safe, so make sure to set passwords that only you know.

>A Fernet Key can be generated with the following command:
>```
>$ python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode("utf-8"))'
>-z10C-HjsdiHJDqq98gzTye-1LES4Kfz3UVouMp6OrA=
>```

You can replace/redefine existing connections from defined from the UI by setting variables like we are doing with `AIRFLOW_CONN_POSTGRES_DEFAULT`. [documentation](https://airflow.apache.org/docs/1.10.10/howto/connection/index.html#storing-a-connection-in-environment-variables)

### Step 2: Get it up and running

Run:
```
docker-compose run --rm webserver initdb; docker-compose up -d
```

After 4 or 5 seconds you should be able to see something at [127.0.0.1:8080](http://127.0.0.1:8080).


## Snippets

**check the tables were created**

`docker-compose exec postgres psql -U airflow airflow -c '\dt'`


**to run any commands inside the postgres container** _(of course you can change it to `webserver`/`scheduler`/`worker`)_

`docker-compose exec postgres bash`


**check the logs generated by the scheduler** _(of course you can also change it to `webserver`/`worker`/`postgres`)_

`docker-compose logs -ft scheduler`

**start over**

`docker-compose down -v; docker-compose run --rm webserver initdb; docker-compose up -d`

  - _The `-v` on the first command takes care of removing the volumes._

  - _The `--rm` is creating a temporary container to run `initdb` required by Airflow._

  - _The `-d` gonna make docker-compose spin up the containers in the background._

**force a restart on the scheduler to kick in a DAG/task execution faster.**

`docker-compose restart scheduler`

**airflow backfill**

`docker-compose exec webserver airflow backfill -x -s'2020-05-05T00:40:00' -e'2020-05-05T00:40:00' --task_regex say_hi test_dag`


## Known issues

`airflow run` is apparently not supported (at least I couldn't get it working :disappointed:)
