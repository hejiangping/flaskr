drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username string not null,
  password string not null
);