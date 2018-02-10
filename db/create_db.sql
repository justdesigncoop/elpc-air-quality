-- 
-- Set character set the client will use to send SQL statements to the server
--
SET NAMES 'utf8';

--
-- Drop database "elpc_air_quality"
--
DROP DATABASE IF EXISTS elpc_air_quality;

--
-- Create database "elpc_air_quality"
--
CREATE DATABASE IF NOT EXISTS elpc_air_quality
	CHARACTER SET utf8
	COLLATE utf8_general_ci;

--
-- Set default database
--
USE elpc_air_quality;

--
-- Drop table "sessions"
--
DROP TABLE IF EXISTS sessions;

--
-- Create table "sessions"
--
CREATE TABLE sessions (
  id INT(11) NOT NULL,
  username VARCHAR(40) NOT NULL,
  start_time_local DATE NOT NULL,
  end_time_local DATE NOT NULL,
  title VARCHAR(40) NOT NULL,
  type VARCHAR(40) NOT NULL,
  PRIMARY KEY (id)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;