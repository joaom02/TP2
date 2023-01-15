CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS POSTGIS;
CREATE EXTENSION IF NOT EXISTS POSTGIS_TOPOLOGY;

CREATE TABLE public.cities (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	latitude		DECIMAL(8,6) DEFAULT  NULL,
	longitude		DECIMAL(9,6) DEFAULT NULL,
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.jobs (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	companyid 		uuid,
	cityref         uuid,
	summary			VARCHAR(10000),
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.companies (
	id              uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name            VARCHAR(250) NOT NULL,
	rating         	VARCHAR(6),
	created_on      TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_on      TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE jobs
    ADD CONSTRAINT jobs_cities_id_fk
        FOREIGN KEY (cityref) REFERENCES cities
            ON DELETE CASCADE;

ALTER TABLE jobs
    ADD CONSTRAINT jobs_companies_id_fk
        FOREIGN KEY (companyid) REFERENCES companies



