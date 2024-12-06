





CREATE TABLE IF NOT EXISTS licenses (
    license_id integer NOT NULL,
    software_name character varying(100),
    license_key character varying(255) NOT NULL,
    allocated_to_user integer
);




    
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;







CREATE TABLE IF NOT EXISTS tickets (
    ticket_id integer NOT NULL,
    user_id integer,
    software_name character varying(100),
    ticket_status character varying(50) DEFAULT 'open',
    request_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    request_type character varying(50) DEFAULT 'general',
    ticket_priority character varying
);




    
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;







CREATE TABLE IF NOT EXISTS users (
    user_id integer NOT NULL,
    username character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    password_hash character varying(255) NOT NULL,
    is_admin boolean DEFAULT false
);




    
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



















44	2		Open	2024-12-03 12:49:56.256072	password_reset	Urgent



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












ALTER TABLE licenses



ALTER TABLE tickets



ALTER TABLE users



ALTER TABLE users



ALTER TABLE licenses



ALTER TABLE tickets



