CREATE SCHEMA IF NOT EXISTS weather;

CREATE TABLE IF NOT EXISTS weather.weather_measurements (
	id BIGSERIAL PRIMARY KEY,
	city VARCHAR(100) NOT NULL,
	latitude NUMERIC(8,5) NOT NULL,
	longitude NUMERIC(8,5) NOT NULL,
	temperature NUMERIC(5,2),
	humidity INTEGER,
	pressure INTEGER,
	wind_speed NUMERIC(5,2),
	observation_time TIMESTAMP NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);