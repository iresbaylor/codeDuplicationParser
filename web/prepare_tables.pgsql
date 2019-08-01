DROP TABLE IF EXISTS origins;
DROP TABLE IF EXISTS clusters;
DROP TABLE IF EXISTS commits;
DROP TABLE IF EXISTS repos;
DROP INDEX IF EXISTS states_name_index;
DROP TABLE IF EXISTS states;

CREATE TABLE states (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);

INSERT INTO states (name, description) VALUES
    ('queue', 'The repository has been added to the queue.'),
    ('invalid', 'This is not a valid repository.'),
    ('done', 'The repository has been successfully analyzed.');

CREATE INDEX states_name_index ON states (name);

CREATE TABLE repos (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    "server" TEXT NOT NULL,
    "user" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    dir TEXT UNIQUE NOT NULL,
    status INTEGER REFERENCES states(id) NOT NULL,
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
    col_offset INTEGER, -- column offset (number of characters on the same line before the token)
    similarity FLOAT NOT NULL,
    UNIQUE(cluster_id, file, line, col_offset)
);
