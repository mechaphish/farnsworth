set client_min_messages to WARNING;

drop database if exists farnsworth;
create database farnsworth;

\c farnsworth;

start transaction;

-- Trees
create extension ltree;

-- Tables that are append-only should inherit from this table.
drop table if exists base;
create table base (
    id bigserial primary key,
    created_on timestamp not null default current_timestamp
);

-- Tables that can be updated should inherit from this table.
drop table if exists updateable;
create table updateable (
    updated_on timestamp not null default current_timestamp
) inherits (base);

---------------------------------------------------------------------

-- Teams
drop table if exists teams;
create table teams (
    name varchar(256) not null,
    unique (id)
) inherits (base);

-- Challenge Tree Nodes
drop table if exists challenge_tree_nodes;
create table challenge_tree_nodes (
    cb_id bigint null,
    parent_id bigint null,
    parent_path ltree null,
    data bytea,
    -- Unique is required to properly work with ltree
    unique (id)
) inherits (base);

-- We have to create the self-references here because of inheritance.
alter table challenge_tree_nodes add
    foreign key (cb_id) references challenge_tree_nodes (id);

alter table challenge_tree_nodes add
    foreign key (parent_id) references challenge_tree_nodes (id);

-- Jobs
drop table if exists jobs;
create table jobs (
    priority int not null default 0,
    started_at timestamp null,
    completed_at timestamp null,
    ctn_id bigint not null references challenge_tree_nodes (id),
    produced_output boolean null,
    unique (id)
) inherits (updateable);

-- Tests
drop type if exists test_type;
create type test_type as enum('unknown', 'test', 'crash', 'exploit1', 'exploit2');

drop table if exists tests;
create table tests (
    ctn_id bigint not null references challenge_tree_nodes (id),
    job_id bigint not null references jobs (id),
    type test_type not null,
    data bytea,
    unique (id)
) inherits (updateable);

-- Rounds
drop table if exists rounds;
create table rounds (
    ends_at timestamp null,
    unique (id)
) inherits (updateable);

-- Scores
drop table if exists scores;
create table scores (
    test_id bigint not null references tests (id),
    round_id bigint not null references rounds (id),
    score_predicted float null,
    score_actual float null
) inherits (updateable);

-- PCAPs
drop type if exists pcap_type;
create type pcap_type as enum('unknown', 'test', 'crash', 'exploit');

drop table if exists pcaps;
create table pcaps (
    ctn_id bigint not null references challenge_tree_nodes (id),
    team_id bigint not null references teams (id),
    round_id bigint not null references rounds (id),
    type pcap_type not null default 'unknown'
) inherits (updateable);

-- Performances
drop table if exists performances;
create table performances (
    test_id bigint not null references tests (id)
    -- TODO: add raw performance measures
) inherits (base);

commit;
