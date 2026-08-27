# Variables
APP=devops-pro
IMAGE=$(APP):latest

# Levantar API local
run:
    uvicorn app.main:app --reload

# Levantar worker local
worker:
    python app/worker.py

# Instalar dependencias
install:
    pip install -r requirements.txt

# Correr tests
test:
    pytest -q

# Correr pre-commit
lint:
    pre-commit run --all-files

# Levantar todo con Docker Compose
up:
    docker-compose up --build

# Apagar servicios
down:
    docker-compose down

# Construir imagen Docker
build:
    docker build -t $(IMAGE) .

# Limpiar caché de Docker
clean:
    docker system prune -f
