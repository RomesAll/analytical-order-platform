#!/bin/bash
set -e

echo "========================================="
echo "ИНИЦИАЛИЗАЦИЯ МАСТЕРА"
echo "========================================="

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- 1. СОЗДАЕМ ПОЛЬЗОВАТЕЛЯ ДЛЯ РЕПЛИКАЦИИ (если не существует)
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '${REPLICATION_USER}') THEN
            CREATE USER ${REPLICATION_USER} WITH REPLICATION ENCRYPTED PASSWORD '${REPLICATION_PASSWORD}';
            RAISE NOTICE 'Пользователь ${REPLICATION_USER} создан';
        ELSE
            RAISE NOTICE 'Пользователь ${REPLICATION_USER} уже существует';
        END IF;
    END
    \$\$;

    -- 2. СОЗДАЕМ СЛОТЫ ДЛЯ РЕПЛИК (если не существуют)
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_replication_slots WHERE slot_name = '${REPLICA1_SLOT}') THEN
            PERFORM pg_create_physical_replication_slot('${REPLICA1_SLOT}');
            RAISE NOTICE 'Слот ${REPLICA1_SLOT} создан';
        ELSE
            RAISE NOTICE 'Слот ${REPLICA1_SLOT} уже существует';
        END IF;
    END
    \$\$;

    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_replication_slots WHERE slot_name = '${REPLICA2_SLOT}') THEN
            PERFORM pg_create_physical_replication_slot('${REPLICA2_SLOT}');
            RAISE NOTICE 'Слот ${REPLICA2_SLOT} создан';
        ELSE
            RAISE NOTICE 'Слот ${REPLICA2_SLOT} уже существует';
        END IF;
    END
    \$\$;

    -- 3. ДАЕМ ПРАВА
    GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO ${REPLICATION_USER};
    GRANT USAGE ON SCHEMA public TO ${REPLICATION_USER};
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO ${REPLICATION_USER};
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ${REPLICATION_USER};

    -- 4. ВЫВОДИМ ИНФОРМАЦИЮ
    \echo 'Пользователь ${REPLICATION_USER} настроен'
    \echo 'Слоты: ${REPLICA1_SLOT}, ${REPLICA2_SLOT}'
EOSQL

echo "========================================="
echo "ИНИЦИАЛИЗАЦИЯ МАСТЕРА ЗАВЕРШЕНА"
echo "========================================="