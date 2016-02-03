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

-- Challenge Tree Nodes
drop table if exists challenge_tree_nodes;
create table challenge_tree_nodes (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    root_id bigint null,
    parent_id bigint null,
    parent_path ltree null,
    name varchar(256) not null,
    blob bytea,
    unique (name)
);

-- We have to create the self-references here because of inheritance.
alter table challenge_tree_nodes add
    foreign key (root_id) references challenge_tree_nodes (id);

alter table challenge_tree_nodes add
    foreign key (parent_id) references challenge_tree_nodes (id);

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
    ctn_id bigint not null references challenge_tree_nodes (id),
    produced_output boolean null,
    blob bytea
);

-- Tests
drop type if exists test_type;
create type test_type as enum('unknown', 'test', 'crash', 'exploit1', 'exploit2');

drop table if exists tests;
create table tests (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    ctn_id bigint not null references challenge_tree_nodes (id),
    job_id bigint not null references jobs (id),
    type test_type not null,
    blob bytea
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
    ctn_id bigint not null references challenge_tree_nodes (id),
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
    ctn_id bigint not null references challenge_tree_nodes (id),
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
