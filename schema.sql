CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE threads (
    id INTEGER PRIMARY KEY,
    peliaika TEXT,
    pelipaikka TEXT,
    pelitaso TEXT,
    pelaajien_maara INTEGER,
    kesto INTEGER,
    user_id INTEGER REFERENCES users
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    status INTEGER DEFAULT 1
);

CREATE TABLE participants (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    thread_id INTEGER REFERENCES threads,
    UNIQUE(user_id, thread_id)
);

CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE INDEX idx_thread_messages ON messages (thread_id);