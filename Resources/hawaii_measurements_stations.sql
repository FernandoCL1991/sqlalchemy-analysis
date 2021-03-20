-- HAWAII_MEASUREMENTS.CSV DATA FRAME
-- Drop table
DROP TABLE IF EXISTS measurements;
-- Creating table
CREATE TABLE measurements (
	station VARCHAR NOT NULL,
	date DATE,
	prcp FLOAT,
	tobs INT
);
SELECT * FROM measurements;

-- HAWAII_STATIONS.CSV DATA FRAME
-- Drop table
DROP TABLE IF EXISTS stations;
-- Creating table
CREATE TABLE stations (
	station VARCHAR (255) NOT NULL,
	name VARCHAR (255),
	latitude FLOAT,
	longitude FLOAT,
	elevation FLOAT
);
SELECT * FROM stations;