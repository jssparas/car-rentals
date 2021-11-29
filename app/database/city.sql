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

SET search_path = public, pg_catalog;

BEGIN TRANSACTION;
ALTER TABLE rental_zone DROP CONSTRAINT rental_zone_city_id_fkey;
TRUNCATE table city;

INSERT INTO public.city (id, created_on, name) values (1, '2021-11-23 12:09:42.269158', 'agra');
INSERT INTO public.city (id, created_on, name) values (2, '2021-11-23 12:09:42.269158', 'noida');
INSERT INTO public.city (id, created_on, name) values (3, '2021-11-23 12:09:42.269158', 'delhi');
INSERT INTO public.city (id, created_on, name) values (4, '2021-11-23 12:09:42.269158', 'mumbai');
INSERT INTO public.city (id, created_on, name) values (5, '2021-11-23 12:09:42.269158', 'lucknow');
INSERT INTO public.city (id, created_on, name) values (6, '2021-11-23 12:09:42.269158', 'chennai');
INSERT INTO public.city (id, created_on, name) values (7, '2021-11-23 12:09:42.269158', 'banglore');
INSERT INTO public.city (id, created_on, name) values (8, '2021-11-23 12:09:42.269158', 'kanpur');


SELECT pg_catalog.setval('public.city_id_seq', 8, true);
ALTER TABLE rental_zone ADD CONSTRAINT rental_zone_city_id_fkey FOREIGN KEY (city_id) REFERENCES city(id);

END;
