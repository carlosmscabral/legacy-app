CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT DEFAULT 'General'
);

INSERT INTO users (name, email, department) VALUES ('Alice', 'alice@example.com', 'Engineering');
INSERT INTO users (name, email, department) VALUES ('Bob', 'bob@example.com', 'Sales');
