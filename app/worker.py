import os
import time

import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))


def get_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def main():
    r = get_redis()
    print("Worker iniciado, escuchando tareas...")

    while True:
        task = r.lpop("task_queue")  # sacar la primera tarea de la cola

        if task:
            print(f"Procesando tarea: {task.decode()}")
            time.sleep(2)  # simula trabajo real
            print("Tarea procesada")
        else:
            time.sleep(1)  # si no hay tareas, espera un segundo


if __name__ == "__main__":
    main()
