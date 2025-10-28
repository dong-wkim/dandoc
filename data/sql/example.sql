CREATE TABLE IF NOT EXISTS example (
    id SERIAL PRIMARY KEY,
    study_id VARCHAR,
    authors VARCHAR,
    title VARCHAR,
    abstract VARCHAR,
    year VARCHAR,
    doi VARCHAR,
    source VARCHAR
);