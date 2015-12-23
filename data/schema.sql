DROP TABLE IF EXISTS todos;

CREATE TABLE todos (
    todo_id INTEGER PRIMARY KEY,
    title TEXT,
    text TEXT,
    done INTEGER,
    pub_date DATETIME
);

insert into todos values (1, 'Hello', 'World', 0, '2015-12-23 00:00:00');
insert into todos values (2, 'Hello Again', 'To World', 1, '2015-12-23 01:01:01');