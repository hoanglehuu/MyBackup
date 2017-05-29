-- DB separation SQL dump

-- No6 table
DROP TABLE cache_entry;
CREATE TABLE cache_entry (
    id integer NOT NULL,
    timecache timestamp without time zone,
    priority integer,
    context character varying(512),
    exten character varying(80)
);

-- No7 table
DROP TABLE dundi_packet;
CREATE TABLE dundi_packet (
    id integer NOT NULL,
    timeoutwhen bigint,
    timeout integer,
    funccb integer,
    pack_ptr bigint,
    retrans integer
);


-- No7 table
DROP TABLE dundi_peer;
CREATE TABLE dundi_peer (
    id integer NOT NULL,
    timeoutwhen bigint,
    timeout integer,
    funccb integer,
    peer_ptr bigint
);

-- No7 table
DROP TABLE dundi_transaction;
CREATE TABLE dundi_transaction (
    id integer NOT NULL,
    timeoutwhen bigint,
    timeout integer,
    funccb integer,
    trans_ptr bigint
);

-- No3 table
DROP TABLE sched_ast_cc_agent;
CREATE TABLE sched_ast_cc_agent (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);

-- No3 table
DROP TABLE sched_ast_cc_monitor;
CREATE TABLE sched_ast_cc_monitor (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);

-- No3 table
DROP TABLE sched_ast_rtp_instance;
CREATE TABLE sched_ast_rtp_instance (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);

-- No3 table
DROP TABLE sched_mwi_subscription_data;
CREATE TABLE sched_mwi_subscription_data (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);

-- No3 table
DROP TABLE sched_network_change;
CREATE TABLE sched_network_change (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);

-- No3 table
DROP TABLE sched_reregister_data;
CREATE TABLE sched_reregister_data (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);


-- No3 table
DROP TABLE sched_sip_esc_entry;
CREATE TABLE sched_sip_esc_entry (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);


-- No3 table
DROP TABLE sched_sip_peer;
CREATE TABLE sched_sip_peer (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);

-- No3 table
DROP TABLE sched_sip_pkt;
CREATE TABLE sched_sip_pkt (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);


-- No3 table
DROP TABLE sched_sip_pvt;
CREATE TABLE sched_sip_pvt (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);


-- No3 table
DROP TABLE sched_sip_registry;
CREATE TABLE sched_sip_registry (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);


ALTER TABLE sched_sip_registry OWNER TO postgres;


-- No3 table
DROP TABLE sched_sip_scheddestroy_data;
CREATE TABLE sched_sip_scheddestroy_data (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);


-- No3 table
DROP TABLE sched_sip_subscription_mwi;
CREATE TABLE sched_sip_subscription_mwi (
    id integer NOT NULL,
    timeoutwhen bigint,
    resched integer,
    variable smallint DEFAULT 0,
    data_ptr bigint,
    funccb integer,
    deleted smallint DEFAULT 0
);

-- No9 table
DROP TABLE subscription_mwi_list;
CREATE TABLE subscription_mwi_list (
    username character varying(512) NOT NULL,
    authuser character varying(512),
    hostname character varying(512) NOT NULL,
    secret character varying(512),
    mailbox character varying(512) NOT NULL,
    transport smallint,
    portno integer,
    resub integer,
    subscribed smallint,
    id character varying(20)
);

-- No8 table
DROP TABLE tcptls_packet;
CREATE TABLE tcptls_packet (
    id bigserial NOT NULL,
    tkey integer NOT NULL,
    data text,
    len integer
);

-- No8 table
DROP TABLE tcptls_session;
CREATE TABLE tcptls_session (
    id integer NOT NULL,
    remote_address character varying(128),
    client integer
);


-- No8 table
DROP TABLE threadinfo;
CREATE TABLE threadinfo (
    id integer NOT NULL,
    alert_pipe0 bigint,
    alert_pipe1 bigint,
    threadid bigint,
    tcptls_session bigint,
    type smallint
);

-- No6 table
DROP TABLE variable_entry;
CREATE TABLE variable_entry (
    id bigserial NOT NULL,
    cacheid integer NOT NULL,
    name character varying(512),
    value character varying(512),
    file character varying(512)
);

-- End dump

-- No6 setup SQL
DROP TABLE extensions;
CREATE TABLE extensions (
    id bigserial NOT NULL,
    context character varying(40) NOT NULL,
    exten character varying(40) NOT NULL,
    priority integer NOT NULL,
    app character varying(40) NOT NULL,
    appdata character varying(256) NOT NULL
);

