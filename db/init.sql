CREATE USER repl WITH replication ENCRYPTED PASSWORD 'kali';
SELECT pg_create_physical_replication_slot('replication_slot');
CREATE TABLE IF NOT EXISTS emails (id SERIAL PRIMARY KEY, mails VARCHAR(100));
CREATE TABLE IF NOT EXISTS phone_numbers (id SERIAL PRIMARY KEY, numbers VARCHAR(100));
INSERT INTO emails (mails) VALUES ('sova.23@mail.ru');
INSERT INTO phone_numbers (numbers) VALUES ('89354632899');
