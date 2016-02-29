set client_min_messages to WARNING;

drop database if exists farnsworth;
create database farnsworth;

\c farnsworth;

start transaction;

-- Trees
create extension ltree;

---------------------------------------------------------------------

-- Teams
drop table if exists teams;
create table teams (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    name varchar(256) not null
);

-- Challenge Binary Nodes
drop table if exists challenge_binary_nodes;
create table challenge_binary_nodes (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    root_id bigint null,
    parent_id bigint null,
    parent_path ltree null,
    name varchar(256) not null,
    blob bytea
);

-- We have to create the self-references here because of inheritance.
alter table challenge_binary_nodes add
    foreign key (root_id) references challenge_binary_nodes (id);

alter table challenge_binary_nodes add
    foreign key (parent_id) references challenge_binary_nodes (id);

-- Jobs
drop table if exists jobs;
create table jobs (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    priority int not null default 0,
    worker varchar(256) not null,
    limit_cpu int null default 4,
    limit_memory int null default 8192,  -- In MB
    started_at timestamp null,
    completed_at timestamp null,
    cbn_id bigint not null references challenge_binary_nodes (id),
    produced_output boolean null,
    payload bytea
);

-- Tests
drop table if exists tests;
create table tests (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    cbn_id bigint not null references challenge_binary_nodes (id),
    job_id bigint not null references jobs (id),
    drilled boolean not null default false,
    blob bytea
);

-- Crashes
drop table if exists crashes;
create table crashes (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    cbn_id bigint not null references challenge_binary_nodes (id),
    job_id bigint not null references jobs (id),
    triaged boolean not null default false,
    explorable boolean null,
    explored boolean null,
    exploitable boolean null,
    exploited boolean null,
    blob bytea
);

-- Exploits
drop type if exists pov_type;
create type pov_type as enum('type1', 'type2');

drop table if exists exploits;
create table exploits (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    cbn_id bigint not null references challenge_binary_nodes (id),
    job_id bigint not null references jobs (id),
    pov_type pov_type not null,
    payload bytea
);

-- Rounds
drop table if exists rounds;
create table rounds (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    ends_at timestamp null
);

-- Scores
drop table if exists scores;
create table scores (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    test_id bigint not null references tests (id),
    round_id bigint not null references rounds (id),
    score_predicted float null,
    score_actual float null
);

-- Bitmaps
drop table if exists bitmaps;
create table bitmaps (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    cbn_id bigint not null references challenge_binary_nodes (id),
    blob bytea
);

-- PCAPs
drop type if exists pcap_type;
create type pcap_type as enum('unknown', 'test', 'crash', 'exploit');

drop table if exists pcaps;
create table pcaps (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    cbn_id bigint not null references challenge_binary_nodes (id),
    team_id bigint not null references teams (id),
    round_id bigint not null references rounds (id),
    type pcap_type not null default 'unknown'
);

-- Performances
drop table if exists performances;
create table performances (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    test_id bigint not null references tests (id)
    -- TODO: add raw performance measures
);

commit;
