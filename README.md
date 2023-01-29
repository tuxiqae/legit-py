# KeyCloak Realm Creator

## What is KeyCloak?
Keycloak is an open-source identity and access management solution that provides features such as authentication, authorization, and user management.

## What are KeyCloak Realms?
Realms in Keycloak are a way to separate different parts of your application or different projects, each with its own set of users, roles, and clients. They provide a way to organize and manage the security settings for your application.

## Description



## Instructions
Install Docker, Docker Compose using your favorite package manage 🐳 
[Click Here!](https://docs.docker.com/compose/install/)

Create the following .env variables under ./env/:
(Not the most elegant solution, would certainly prefer to use a secret management system such as HashiCorp Vault)

- env/.postgres:
```env
POSTGRES_DB=keycloak
POSTGRES_USER=keycloak
POSTGRES_PASSWORD=password
```

- env/.keycloak:
```env
DB_VENDOR=POSTGRES
DB_ADDR=<DB address>
DB_DATABASE=<DB name>
DB_USER=<DB username>
DB_PASSWORD=<DB password>
```

- env/.credentials:
```env
KEYCLOAK_USER=admin
KEYCLOAK_PASSWORD=admin
```

- env/.env:
Should already be included as it contains no sensitive information, but should look like that
```env
APP_NAME=legit-py
VERSION=0.1.0
APP_PORT=8000
APP_BIND_ADDR=0.0.0.0

KC_PORT=8080
```

🙌 Run the command `docker compose --file docker-compose.yml --env-file --env-file env/.env up --build` and you should be good to go! 🙌

You can then trigger the REST API in order to create new realms:
```
⤅ curl -X POST "http://localhost:8000/realms/foo"
{"message":"Created realm 'foo'"}

⤅ curl -X POST "http://localhost:8000/realms/foo"
{"message":"Realm 'foo' already exists in the system."}

⤅ curl -X POST "http://localhost:8000/realms/bar"
{"message":"Created realm 'bar'"}
```

You can also read more in our [API documentation](http://<addr>/redoc) or in our cool [SwaggerUI](http://<addr>/doc)

## Removal
Run the command `docker compose --file docker-compose.yml --env-file env/.env down --remove-orphans --volumes`

