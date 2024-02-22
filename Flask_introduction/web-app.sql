CREATE TABLE region (
	id integer PRIMARY KEY UNIQUE,
	name varchar(255) NOT NULL
)

CREATE TABLE tax_param (
	id serial PRIMARY KEY UNIQUE,
	city_id integer NOT NULL REFERENCES region(id),
	from_hp_car integer NOT NULL,
	to_hp_car integer NOT NULL,
	from_production_year_car integer NOT NULL,
	to_production_year_car integer NOT NULL,
	rate numeric NOT NULL
)

CREATE TABLE auto (
	id serial PRIMARY KEY UNIQUE,
	city_id integer NOT NULL REFERENCES region(id),
	tax_id integer NOT NULL REFERENCES tax_param(id),
	name varchar(255) NOT NULL,
	horse_power integer NOT NULL,
	production_year integer NOT NULL,
	tax numeric NOT NULL
)