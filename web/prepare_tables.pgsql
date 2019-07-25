DROP TABLE IF EXISTS clones;
DROP TABLE IF EXISTS clusters;
DROP TABLE IF EXISTS commits;
DROP TABLE IF EXISTS repos;

CREATE TABLE repos (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    dir TEXT UNIQUE NOT NULL,
    "server" TEXT NOT NULL,
    "user" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    UNIQUE("server", "user", "name")
);

CREATE TABLE commits (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES repos(id) NOT NULL,
    hash TEXT NOT NULL,
    finished BOOLEAN NOT NULL DEFAULT FALSE,
    date TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE(repo_id, hash)
);

CREATE TABLE clusters (
    id SERIAL PRIMARY KEY,
    commit_id INTEGER REFERENCES commits(id) NOT NULL,
    "value" TEXT NOT NULL,
    weight INTEGER NOT NULL
);

CREATE TABLE clones (
    id SERIAL PRIMARY KEY,
    cluster_id INTEGER REFERENCES clusters(id) NOT NULL,
    origin TEXT NOT NULL,
    similarity FLOAT NOT NULL
);
