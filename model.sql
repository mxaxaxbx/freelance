CREATE DATABASE freelance_db;

-- public.services definition

-- Drop table

-- DROP TABLE public.services;

CREATE TABLE public.services (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	CONSTRAINT service_pk PRIMARY KEY (id)
);

-- public.deliverables definition

-- Drop table

-- DROP TABLE public.deliverables;

CREATE TABLE public.deliverables (
	id serial4 NOT NULL,
	"name" varchar NOT NULL,
	"description" text NOT NULL,
	CONSTRAINT deliverable_pk PRIMARY KEY (id)
);

-- public.packages definition

-- Drop table

-- DROP TABLE public.packages;

CREATE TABLE public.packages (
	id serial4 NOT NULL,
	"description" text NOT NULL,
	price float8 NOT NULL,
	deliverables_id int4 NOT NULL,
	service_id int4 NOT NULL,
	CONSTRAINT package_pk PRIMARY KEY (id),
	CONSTRAINT fk_deliverable FOREIGN KEY (deliverables_id) REFERENCES public.deliverables(id),
	CONSTRAINT fk_service FOREIGN KEY (service_id) REFERENCES public.services(id)
);
