CREATE TABLE IF NOT EXISTS example (
    id SERIAL PRIMARY KEY,
    study_id VARCHAR,
    authors VARCHAR,
    title VARCHAR,
    abstract VARCHAR,
    year NUM(4),
    doi VARCHAR,
    source VARCHAR
);