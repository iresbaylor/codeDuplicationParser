DROP TABLE IF EXISTS origins;
DROP TABLE IF EXISTS clusters;
DROP TABLE IF EXISTS commits;
DROP TABLE IF EXISTS repos;

CREATE TABLE repos (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    "server" TEXT NOT NULL,
    "user" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    dir TEXT UNIQUE NOT NULL,
    valid BOOLEAN, -- NULL = validation in progress; FALSE = invalid repo; TRUE = valid and available
    UNIQUE("server", "user", "name")
);

CREATE TABLE commits (
    id SERIAL PRIMARY KEY,
    repo_id INTEGER REFERENCES repos(id) NOT NULL,
    hash TEXT NOT NULL,
    finished BOOLEAN DEFAULT FALSE NOT NULL,
    cloned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
    UNIQUE(repo_id, hash)
);

CREATE TABLE clusters (
    id SERIAL PRIMARY KEY,
    commit_id INTEGER REFERENCES commits(id) NOT NULL,
    "value" TEXT NOT NULL,
    weight INTEGER NOT NULL
);

CREATE TABLE origins (
    id SERIAL PRIMARY KEY,
    cluster_id INTEGER REFERENCES clusters(id) NOT NULL,
    file TEXT NOT NULL,
    line INTEGER,
    offset INTEGER, -- column offset (number of characters on the same line before the token)
    similarity FLOAT NOT NULL,
    UNIQUE(cluster_id, file, line, offset)
);
