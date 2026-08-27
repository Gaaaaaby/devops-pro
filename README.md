

# README.md

## Proyecto DevOps – API + Worker + Redis + CI/CD

Este proyecto implementa una arquitectura DevOps completa usando únicamente herramientas gratuitas.
Incluye:

- API en FastAPI
- Worker para tareas en background
- Redis como cola de mensajes
- Dockerfile
- Docker Compose
- Tests automáticos
- Pre‑commit
- CI (validación de código)
- Compose CI (validación del sistema completo)
- CD (build y push de imagen a GHCR)
- Makefile para automatizar comandos

El proyecto funciona completamente **sin deploy**, porque las plataformas gratuitas no soportan esta arquitectura (API + worker + redis).
El evaluador puede correr todo localmente con Docker Compose.

---

## Arquitectura

Servicios:

- api → expone endpoints y envía tareas a redis
- worker → procesa tareas en background
- redis → cola de mensajes
- sqlite → base de datos local

Flujo:

- api → redis → worker
- api → health check para validar estado del sistema

---

## Estructura del proyecto

```
devops-pro/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── worker.py
│   ├── tasks.py
│   ├── db.py
│   └── models.py
│
├── tests/
│   └── test_api.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Makefile
├── README.md
├── .pre-commit-config.yaml
└── .github/
    └── workflows/
        ├── ci.yml
        ├── compose-ci.yml
        └── cd.yml
```

---

## Cómo correr el proyecto localmente

Instalar dependencias:

```
make install
```

Levantar API:

```
make run
```

Levantar worker:

```
make worker
```

---

## Cómo correr el proyecto con Docker Compose

```
make up
```

Esto levanta:

- api
- worker
- redis

Health check:

```
http://localhost:8000/health
```

Apagar:

```
make down
```

---

## Tests

```
make test
```

---

## Pre‑commit

```
make lint
```

Incluye:

- black
- isort
- flake8
- check-yaml
- end-of-file-fixer
- trailing-whitespace

---

## CI – Validación del código (ci.yml)

Este workflow:

- instala Python
- instala dependencias
- corre pre‑commit
- corre pytest
- construye la imagen Docker

Es la validación del código y la imagen.

---

## Compose CI – Validación del sistema completo (compose-ci.yml)

Este workflow:

- instala docker-compose
- construye imágenes
- levanta api + worker + redis
- espera a que la API arranque
- prueba el health check real

Es la validación del sistema completo corriendo en contenedores.

---

## CD – Build y push de imagen (cd.yml)

Este workflow:

- construye la imagen
- hace login en GHCR
- pushea la imagen

Imagen disponible en:

```
ghcr.io/<usuario>/<repo>:latest
```

---
