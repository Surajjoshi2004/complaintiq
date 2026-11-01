--
-- PostgreSQL database dump
--

\restrict LHuhKMNb761yVfdLf9g8VIaEHc5WlRGkOSqpb5k65ILIy2SDJ7f7062MfuHdxcb

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg13+2)
-- Dumped by pg_dump version 16.15 (Debian 16.15-1.pgdg13+2)

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
-- Name: complaints; Type: TABLE; Schema: public; Owner: complaintiq
--

CREATE TABLE public.complaints (
    id integer NOT NULL,
    customer_id integer NOT NULL,
    complaint_text character varying NOT NULL,
    predicted_category character varying(150) NOT NULL,
    confidence double precision NOT NULL,
    "createdAt" timestamp with time zone NOT NULL
);


ALTER TABLE public.complaints OWNER TO complaintiq;

--
-- Name: complaints_id_seq; Type: SEQUENCE; Schema: public; Owner: complaintiq
--

CREATE SEQUENCE public.complaints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.complaints_id_seq OWNER TO complaintiq;

--
-- Name: complaints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: complaintiq
--

ALTER SEQUENCE public.complaints_id_seq OWNED BY public.complaints.id;


--
-- Name: complaints id; Type: DEFAULT; Schema: public; Owner: complaintiq
--

ALTER TABLE ONLY public.complaints ALTER COLUMN id SET DEFAULT nextval('public.complaints_id_seq'::regclass);


--
-- Data for Name: complaints; Type: TABLE DATA; Schema: public; Owner: complaintiq
--

COPY public.complaints (id, customer_id, complaint_text, predicted_category, confidence, "createdAt") FROM stdin;
1	101	101	Checking or savings account	0.34199668495131247	2026-10-18 16:21:16.025004+00
2	101	101	Checking or savings account	0.34199668495131247	2026-10-18 16:22:15.83532+00
3	202	My bank charged me twice	Checking or savings account	0.2796949747215283	2026-10-18 19:47:44.792039+00
4	101	My bank charged me thrice	Checking or savings account	0.34199668495131247	2026-10-18 20:20:19.389163+00
5	101	My bank charged me thrice	Checking or savings account	0.34199668495131247	2026-10-18 21:09:10.568974+00
6	101	My bank charged me thrice	Checking or savings account	0.34199668495131247	2026-10-19 06:26:18.375027+00
7	101	My bank charged me thrice	Checking or savings account	0.34199668495131247	2026-10-19 06:28:15.847142+00
8	101	My bank charged me thrice	Checking or savings account	0.34199668495131247	2026-10-19 06:30:14.829136+00
\.


--
-- Name: complaints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: complaintiq
--

SELECT pg_catalog.setval('public.complaints_id_seq', 8, true);


--
-- Name: complaints complaints_pkey; Type: CONSTRAINT; Schema: public; Owner: complaintiq
--

ALTER TABLE ONLY public.complaints
    ADD CONSTRAINT complaints_pkey PRIMARY KEY (id);


--
-- Name: ix_complaints_id; Type: INDEX; Schema: public; Owner: complaintiq
--

CREATE INDEX ix_complaints_id ON public.complaints USING btree (id);


--
-- PostgreSQL database dump complete
--

\unrestrict LHuhKMNb761yVfdLf9g8VIaEHc5WlRGkOSqpb5k65ILIy2SDJ7f7062MfuHdxcb

