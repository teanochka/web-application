toc.dat                                                                                             0000600 0004000 0002000 00000005755 14716256230 0014461 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        PGDMP   ,                
    |         	   hackathon    16.2    16.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false         �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false         �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false         �           1262    24627 	   hackathon    DATABASE     }   CREATE DATABASE hackathon WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';
    DROP DATABASE hackathon;
                postgres    false         �            1259    24629    container_sites    TABLE        CREATE TABLE public.container_sites (
    id integer NOT NULL,
    latitude numeric(9,6) NOT NULL,
    longitude numeric(9,6) NOT NULL,
    has_landfill boolean NOT NULL,
    last_disposal_date date NOT NULL,
    description text,
    confirmation_needed boolean,
    images_path text
);
 #   DROP TABLE public.container_sites;
       public         heap    postgres    false         �            1259    24628    container_sites_id_seq    SEQUENCE     �   CREATE SEQUENCE public.container_sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.container_sites_id_seq;
       public          postgres    false    216         �           0    0    container_sites_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.container_sites_id_seq OWNED BY public.container_sites.id;
          public          postgres    false    215         O           2604    24632    container_sites id    DEFAULT     x   ALTER TABLE ONLY public.container_sites ALTER COLUMN id SET DEFAULT nextval('public.container_sites_id_seq'::regclass);
 A   ALTER TABLE public.container_sites ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    216    215    216         �          0    24629    container_sites 
   TABLE DATA           �   COPY public.container_sites (id, latitude, longitude, has_landfill, last_disposal_date, description, confirmation_needed, images_path) FROM stdin;
    public          postgres    false    216       4834.dat �           0    0    container_sites_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.container_sites_id_seq', 10, true);
          public          postgres    false    215         Q           2606    24636 $   container_sites container_sites_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.container_sites
    ADD CONSTRAINT container_sites_pkey PRIMARY KEY (id);
 N   ALTER TABLE ONLY public.container_sites DROP CONSTRAINT container_sites_pkey;
       public            postgres    false    216                           4834.dat                                                                                            0000600 0004000 0002000 00000003322 14716256230 0014262 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        5	1.000000	1.000000	f	2024-11-16		f	uploads/083200_jpg.rf.363000e8604a30d9835d6e7846648023.jpg
2	1.000000	3.000000	t	2024-11-16	шины,бумага	f	uploads/074325_jpg.rf.a5410fb72a1847e71e6e80eee87555c5.jpg,uploads/075100_jpg.rf.1cf35a78f4bd7d3168a6de2a4e09cc02.jpg,uploads/075108_jpg.rf.99c600b00903afc5e9973a2336fa22cc.jpg,uploads/075300_jpg.rf.a1eb1730ea8f9bdeb01ff5806a2326e7.jpg
3	2.000000	3.000000	f	2024-11-16		f	uploads/074325_jpg.rf.a5410fb72a1847e71e6e80eee87555c5.jpg,uploads/075100_jpg.rf.1cf35a78f4bd7d3168a6de2a4e09cc02.jpg,uploads/075108_jpg.rf.99c600b00903afc5e9973a2336fa22cc.jpg,uploads/075300_jpg.rf.a1eb1730ea8f9bdeb01ff5806a2326e7.jpg
4	3.000000	4.000000	f	2024-11-16		t	uploads/083200_jpg.rf.363000e8604a30d9835d6e7846648023.jpg
6	1.000000	2.000000	t	2024-11-17		f	uploads/074325_jpg.rf.a5410fb72a1847e71e6e80eee87555c5.jpg,uploads/075100_jpg.rf.1cf35a78f4bd7d3168a6de2a4e09cc02.jpg,uploads/075108_jpg.rf.99c600b00903afc5e9973a2336fa22cc.jpg,uploads/075300_jpg.rf.a1eb1730ea8f9bdeb01ff5806a2326e7.jpg
7	8.544667	6.544030	f	2024-11-09	Пакеты	f	uploads/075108_jpg.rf.99c600b00903afc5e9973a2336fa22cc.jpg,uploads/075300_jpg.rf.a1eb1730ea8f9bdeb01ff5806a2326e7.jpg
1	2.000000	1.000000	t	2024-11-16		f	uploads/074325_jpg.rf.a5410fb72a1847e71e6e80eee87555c5.jpg,uploads/075100_jpg.rf.1cf35a78f4bd7d3168a6de2a4e09cc02.jpg,uploads/075108_jpg.rf.99c600b00903afc5e9973a2336fa22cc.jpg,uploads/075300_jpg.rf.a1eb1730ea8f9bdeb01ff5806a2326e7.jpg
9	0.000000	0.000000	t	2024-11-17	Пакеты	f	uploads/081236_jpg.rf.395918d5aa6dba6c09a7bc859c02145c.jpg
10	55.709728	37.193454	t	2024-11-17	мебель	f	uploads/083600_jpg.rf.f94c5cca7d261cb75873b75213cbffef.jpg,uploads/084854_jpg.rf.825f18eb5ff9565e77377e17c8729b39.jpg
\.


                                                                                                                                                                                                                                                                                                              restore.sql                                                                                         0000600 0004000 0002000 00000006225 14716256230 0015377 0                                                                                                    ustar 00postgres                        postgres                        0000000 0000000                                                                                                                                                                        --
-- NOTE:
--
-- File paths need to be edited. Search for $$PATH$$ and
-- replace it with the path to the directory containing
-- the extracted data files.
--
--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE hackathon;
--
-- Name: hackathon; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE hackathon WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Russian_Russia.1251';


ALTER DATABASE hackathon OWNER TO postgres;

\connect hackathon

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: container_sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.container_sites (
    id integer NOT NULL,
    latitude numeric(9,6) NOT NULL,
    longitude numeric(9,6) NOT NULL,
    has_landfill boolean NOT NULL,
    last_disposal_date date NOT NULL,
    description text,
    confirmation_needed boolean,
    images_path text
);


ALTER TABLE public.container_sites OWNER TO postgres;

--
-- Name: container_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.container_sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.container_sites_id_seq OWNER TO postgres;

--
-- Name: container_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.container_sites_id_seq OWNED BY public.container_sites.id;


--
-- Name: container_sites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.container_sites ALTER COLUMN id SET DEFAULT nextval('public.container_sites_id_seq'::regclass);


--
-- Data for Name: container_sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.container_sites (id, latitude, longitude, has_landfill, last_disposal_date, description, confirmation_needed, images_path) FROM stdin;
\.
COPY public.container_sites (id, latitude, longitude, has_landfill, last_disposal_date, description, confirmation_needed, images_path) FROM '$$PATH$$/4834.dat';

--
-- Name: container_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.container_sites_id_seq', 10, true);


--
-- Name: container_sites container_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.container_sites
    ADD CONSTRAINT container_sites_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           