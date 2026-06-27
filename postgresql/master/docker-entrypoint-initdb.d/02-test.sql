CREATE TABLE test_replication (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
INSERT INTO test_replication (name) VALUES ('First record');
INSERT INTO test_replication (name) VALUES ('Second record');