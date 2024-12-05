--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: licenses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.licenses (
    license_id integer NOT NULL,
    software_name character varying(100),
    license_key character varying(255) NOT NULL,
    allocated_to_user integer
);


ALTER TABLE public.licenses OWNER TO postgres;

--
-- Name: licenses_license_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.licenses_license_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.licenses_license_id_seq OWNER TO postgres;

--
-- Name: licenses_license_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.licenses_license_id_seq OWNED BY public.licenses.license_id;


--
-- Name: tickets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tickets (
    ticket_id integer NOT NULL,
    user_id integer,
    software_name character varying(100),
    ticket_status character varying(50) DEFAULT 'open'::character varying,
    request_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    request_type character varying(50) DEFAULT 'general'::character varying,
    ticket_priority character varying
);


ALTER TABLE public.tickets OWNER TO postgres;

--
-- Name: tickets_ticket_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tickets_ticket_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tickets_ticket_id_seq OWNER TO postgres;

--
-- Name: tickets_ticket_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tickets_ticket_id_seq OWNED BY public.tickets.ticket_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    password_hash character varying(255) NOT NULL,
    is_admin boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: licenses license_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.licenses ALTER COLUMN license_id SET DEFAULT nextval('public.licenses_license_id_seq'::regclass);


--
-- Name: tickets ticket_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tickets ALTER COLUMN ticket_id SET DEFAULT nextval('public.tickets_ticket_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: licenses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.licenses (license_id, software_name, license_key, allocated_to_user) FROM stdin;
\.


--
-- Data for Name: tickets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tickets (ticket_id, user_id, software_name, ticket_status, request_time, request_type, ticket_priority) FROM stdin;
44	2		Open	2024-12-03 12:49:56.256072	password_reset	Urgent
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, email, password_hash, is_admin) FROM stdin;
274	DeepakRamesh	deepakramesh@gmail.com	scrypt:32768:8:1$KGxb6A13k8EhLAUy$801fca4f604fae04fa7bbf09b37feab87a89f340a386d12b124ef978f524f19c38bda7dd405abc53bd8029d7fb2f9a32fe81e5bfa9da85d7f39319de0b5e45dc	f
2	demo	demo@gmail.com	scrypt:32768:8:1$oL38LYHY1vajYIJ3$bcc5f99e7c5773881f7a651f8779335e1fdc6836d8dd5da5fa985e6080a31e21eba876151cb22d4e20aafaae90ece2c85e83ae1acdf7dc9cad9ef85ec5578361	f
4	DeepakResjad	deepak.resjad@gmail.com	scrypt:32768:8:1$Gv2kfRrlxiVdcLLj$4eb7d8bdd2c4caee1c1468b5cd105f6cdd01f819d947b5b8b97c86febee303d8db52aface56742fecda64752a395f694a787194350d58139b4bace9adb8a6c8b	f
5	nitish	nitishgoud28@gmail.com	scrypt:32768:8:1$Kcl3tHrPiKaQ4nRA$68d316c088f31eb8ee39d26c05efd2db0406c442756137d853f2caf4d65fc1c5e78013b2648cbd3b5f2e073833229051d18fea47c68763d241e9dc5f81ed2e40	f
6	VishalMuniraj	Vishal@gmail.com	scrypt:32768:8:1$of1lHcQABk5ihd14$c45a0183fca9984f6aaab5afc1ec87485ff814096ef262e995e672a329c40ccede29abb72c830b8a614b3e9ff772475a5d507e70f1716992b73de6f5130518c1	f
27	deepak	deepak@gmail.com	scrypt:32768:8:1$Xpf90MLb4cEGnAwV$77b03a93c95f2739e7ed9cced8489c776df585bd28821b5b72ad602b809d5051272f7081cfd7ba4fc88eadff756666a83290cc345b67b7fdf37681491047f9b6	f
270	testuser	test@gmail.com	52bfd2de0a2e69dff4517518590ac32a46bd76606ec22a258f99584a6e70aca2	f
271	Admin	admin@gmail.com	scrypt:32768:8:1$HYrZ7JotKfwfuAkk$c17db4e7bf2b57d91fcc9dc0e68e8c69ea3be92e8d04f455fe358f0db03108c85945fc64772a3c420a10da9eea6f57aaeb3f60d78ffe9e3a98186bd86cfa736a	f
272	Deepakvenkateshwar	deepakvenkateshwar@gmail.com	scrypt:32768:8:1$LNnOY3jX2duoee2I$2c7471ef826205f9885ff606626175622cc31f1355ace61da6424e7ce19684aebd381cb8130b77ad98e49b9667872ef5de5665a1a5dd3cf96771f4345441833d	f
273	deepakvenkateshwar	deepak123@gmail.com	scrypt:32768:8:1$e66lGAzs0QldcGip$a852e5c2bd448106f4417ee4685aaee6d1f7830c5c733e00950b811de222e3528931a4fc382504a5a1ecf4107e2cce352360169eb1e66193f8fb5db472327ae8	f
\.


--
-- Name: licenses_license_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.licenses_license_id_seq', 1, false);


--
-- Name: tickets_ticket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tickets_ticket_id_seq', 44, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 274, true);


--
-- Name: licenses licenses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.licenses
    ADD CONSTRAINT licenses_pkey PRIMARY KEY (license_id);


--
-- Name: tickets tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_pkey PRIMARY KEY (ticket_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: licenses licenses_allocated_to_user_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.licenses
    ADD CONSTRAINT licenses_allocated_to_user_fkey FOREIGN KEY (allocated_to_user) REFERENCES public.users(user_id);


--
-- Name: tickets tickets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tickets
    ADD CONSTRAINT tickets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

