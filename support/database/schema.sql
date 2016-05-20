set client_min_messages to WARNING;

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
    cs_id varchar(256) not null,
    submitted_at timestamp null,
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
    limit_time int null,  -- In Seconds
    started_at timestamp null,
    completed_at timestamp null,
    cbn_id bigint not null references challenge_binary_nodes (id),
    produced_output boolean null,
    payload jsonb
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
    submitted_at timestamp null,
    submitted_teams varchar(256) null,
    blob bytea
);

-- Rounds
drop table if exists rounds;
create table rounds (
    id bigserial primary key,
    num integer not null,
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
    round_id bigint not null references rounds (id),
    scores jsonb
    -- score_predicted float null,
    -- score_actual float null
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

-- Fuzzer Stats
drop table if exists fuzzer_stats;
create table fuzzer_stats (
    id bigserial primary key,
    cbn_id bigint not null references challenge_binary_nodes (id),
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    pending_favs int null default 0,
    pending_total int null default 0,
    paths_total int null default 0,
    paths_found int null default 0,
    last_path timestamp null
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

-- CGC Feedbacks
drop table if exists feedbacks;
create table feedbacks (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    round_id bigint not null references rounds (id),
    polls jsonb,
    cbs jsonb,
    povs jsonb
    -- TODO: add raw performance measures
);

-- CGC consensus evaluation
drop table if exists evaluations;
create table evaluations (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    round_id bigint not null references rounds (id),
    team_id bigint not null references teams (id),
    cbs jsonb,
    ids jsonb
    -- TODO: add raw performance measures
);

-- Tester results.
drop table if exists tester_results;
create table tester_results (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    job_id bigint not null references jobs (id),
    error_code int,
    result varchar(256) null,
    stdout_out text,
    stderr_out text,
    performances jsonb
);

-- Poller results.
drop table if exists valid_polls;
create table valid_polls (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp not null default current_timestamp,
    test_id bigint not null references tests (id),
    cbn_id bigint not null references challenge_binary_nodes (id),
    blob bytea
);

commit;
