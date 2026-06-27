#!/bin/bash
set -e

echo "========================================="
echo "ИНИЦИАЛИЗАЦИЯ РЕПЛИКИ ${REPLICA_NUM}"
echo "========================================="

PGDATA="/var/lib/postgresql/data"

if [ -s "$PGDATA/PG_VERSION" ]; then
  echo "Данные уже есть, пропускаем pg_basebackup"
  echo "Запускаем PostgreSQL"
  exec docker-entrypoint.sh "$@"
fi

# Ждем мастер
echo "Ожидание готовности Мастера"
until PGPASSWORD=${REPLICATION_PASSWORD} pg_isready -h ${PRIMARY_HOST} -U ${REPLICATION_USER}; do
    echo "Мастер еще не готов, ждем 2 секунды"
    sleep 2
done

echo "Мастер готов! Начинаем pg_basebackup"

# Выполняем pg_basebackup
PGPASSWORD=${REPLICATION_PASSWORD} pg_basebackup \
    -h ${PRIMARY_HOST} \
    -p 5432 \
    -U ${REPLICATION_USER} \
    -D ${PGDATA} \
    -X stream \
    -R \
    -v \
    -P \
    -S ${REPLICA_SLOT}

if [ $? -eq 0 ]; then
    echo "pg_basebackup завершен успешно!"
else
    echo "pg_basebackup завершился с ошибкой!"
    exit 1
fi

echo "========================================="
echo "РЕПЛИКА ${REPLICA_NUM} УСПЕШНО ИНИЦИАЛИЗИРОВАНА!"
echo "   Слот: ${REPLICA_SLOT}"
echo "   Мастер: ${PRIMARY_HOST}"
echo "========================================="

exec docker-entrypoint.sh "$@"