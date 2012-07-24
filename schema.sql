drop table if exists events;
create table events (
    key string not null,
    value float not null,
    ts float not null
);
