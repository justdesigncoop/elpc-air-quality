-- 
-- Set character set the client will use to send SQL statements to the server
--
SET NAMES 'utf8';

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
-- Drop table "users"
--
DROP TABLE IF EXISTS users;

--
-- Create table "users"
--
CREATE TABLE users (
  id INT(11),
  username VARCHAR(40) NOT NULL,
  PRIMARY KEY (username),
  INDEX index_users_on_id (id)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Drop table "sessions"
--
DROP TABLE IF EXISTS sessions;

--
-- Create table "sessions"
--
CREATE TABLE sessions (
  id INT(11) NOT NULL,
  created_at DATETIME,
  updated_at DATETIME,
  user_id INT,
  uuid VARCHAR(40),
  url_token VARCHAR(40),
  title TEXT,
  description TEXT,
  calibration INT,
  contribute BOOLEAN,
  data_type VARCHAR(40),
  instrument VARCHAR(40),
  phone_model VARCHAR(40),
  os_version VARCHAR(40),
  offset_60_db VARCHAR(40),
  start_time DATETIME,
  end_time DATETIME,
  measurements_count INT,
  timezone_offset INT,
  start_time_local DATETIME,
  end_time_local DATETIME,
  type VARCHAR(40) NOT NULL,
  is_indoor BOOLEAN,
  latitude DOUBLE,
  longitude DOUBLE,
  last_measurement_at DATETIME,
  PRIMARY KEY (id),
  INDEX index_sessions_on_contribute (contribute),
  INDEX index_sessions_on_end_time (end_time),
  INDEX index_sessions_on_local_end_time (end_time_local),
  INDEX index_sessions_on_last_measurement_at (last_measurement_at),
  INDEX index_sessions_on_start_time (start_time),
  INDEX index_sessions_on_local_start_time (start_time_local),
  INDEX index_sessions_on_url_token (url_token),
  INDEX index_sessions_on_user_id (user_id),
  INDEX index_sessions_on_uuid (uuid),
  CONSTRAINT constrain_session_on_user_id FOREIGN KEY (user_id)
    REFERENCES users(id) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Drop table "notes"
--
DROP TABLE IF EXISTS notes;

--
-- Create table "notes"
--
CREATE TABLE notes (
  id INT(11) NOT NULL,
  created_at DATETIME,
  updated_at DATETIME,
  date DATETIME,
  text TEXT,
  latitude DOUBLE,
  longitude DOUBLE,
  session_id INT(11),
  photo_file_name VARCHAR(40),
  photo_content_type VARCHAR(40),
  photo_file_size INT(11),
  photo_updated_at DATETIME,
  number INT(11),
  photo TEXT,
  photo_thumbnail TEXT,
  PRIMARY KEY (id),
  INDEX index_notes_on_session_id (session_id),
  CONSTRAINT constrain_notes_on_session_id FOREIGN KEY (session_id)
    REFERENCES sessions(id) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Drop table "streams"
--
DROP TABLE IF EXISTS streams;

--
-- Create table "streams"
--
CREATE TABLE streams (
  id INT(11) NOT NULL,
  sensor_name VARCHAR(40),
  unit_name VARCHAR(40),
  measurement_type VARCHAR(40),
  measurement_short_type VARCHAR(40),
  unit_symbol VARCHAR(40),
  threshold_very_low INT(11),
  threshold_low INT(11),
  threshold_medium INT(11),
  threshold_high INT(11),
  threshold_very_high INT(11),
  session_id INT(11),
  sensor_package_name VARCHAR(40) DEFAULT "Builtin" NOT NULL,
  measurements_count INT(11) DEFAULT 0 NOT NULL,
  min_latitude DOUBLE,
  max_latitude DOUBLE,
  min_longitude DOUBLE,
  max_longitude DOUBLE,
  average_value FLOAT,
  PRIMARY KEY (id),
  INDEX index_streams_on_max_latitude (max_latitude),
  INDEX index_streams_on_max_longitude (max_longitude),
  INDEX index_streams_on_min_latitude (min_latitude),
  INDEX index_streams_on_min_longitude (min_longitude),
  INDEX index_streams_on_sensor_name_and_measurement_type (sensor_name, measurement_type),
  INDEX index_streams_on_sensor_name (sensor_name),
  INDEX index_streams_on_session_id (session_id),
  CONSTRAINT constrain_streams_on_session_id FOREIGN KEY (session_id)
    REFERENCES sessions(id) ON DELETE CASCADE ON UPDATE RESTRICT
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Drop table "wards"
--
DROP TABLE IF EXISTS wards;

--
-- Create table "wards"
--
CREATE TABLE wards (
  ward INT(11) NOT NULL,
  geo LONGTEXT,
  PRIMARY KEY (ward)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Insert default ward
--
INSERT INTO wards (ward, geo) VALUES (0, 'MULTIPOLYGON EMPTY');

--
-- Drop table "neighborhoods"
--
DROP TABLE IF EXISTS neighborhoods;

--
-- Create table "neighborhoods"
--
CREATE TABLE neighborhoods (
  id INT(11) NOT NULL AUTO_INCREMENT,
  neighborhood VARCHAR(40),
  geo LONGTEXT,
  PRIMARY KEY (id),
  INDEX index_neighborhoods_on_neighborhood (neighborhood)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Insert default neighborhood
--
INSERT INTO neighborhoods (id, neighborhood, geo) VALUES (0, 'None', 'MULTIPOLYGON EMPTY');

--
-- Drop table "census"
--
DROP TABLE IF EXISTS census;

--
-- Create table "census"
--
CREATE TABLE census (
  tract BIGINT(11) NOT NULL,
  geo LONGTEXT,
  PRIMARY KEY (tract)
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;

--
-- Insert default tract
--
INSERT INTO census (tract, geo) VALUES (0, 'MULTIPOLYGON EMPTY');

--
-- Drop table "measurements"
--
DROP TABLE IF EXISTS measurements;

--
-- Create table "measurements"
--
CREATE TABLE measurements (
  id INT(11) NOT NULL,
  value FLOAT,
  latitude DOUBLE,
  longitude DOUBLE,
  time DATETIME,
  timezone_offset INT(11),
  stream_id INT(11),
  milliseconds INT(11) DEFAULT 0,
  measured_value FLOAT,
  created_at DATETIME,
  ward_id INT(11),
  neighborhood_id INT(11),
  tract_id BIGINT(11),
  PRIMARY KEY (id, stream_id),
  INDEX index_measurements_on_latitude (latitude),
  INDEX index_measurements_on_longitude_and_latitude (latitude, longitude),
  INDEX index_measurements_on_longitude (longitude),
  INDEX index_measurements_on_stream_id (stream_id),
  INDEX index_measurements_on_time (time),
  INDEX index_measurements_on_ward (ward),
  INDEX index_measurements_on_neighborhood (neighborhood),
  INDEX index_measurements_on_tract (tract),
  CONSTRAINT constrain_measurements_on_stream_id FOREIGN KEY (stream_id)
    REFERENCES streams(id) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT constrain_measurements_on_ward FOREIGN KEY (ward)
    REFERENCES wards(ward) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT constrain_measurements_on_neighborhood FOREIGN KEY (neighborhood)
    REFERENCES neighborhoods(id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT constrain_measurements_on_census_tract FOREIGN KEY (tract)
    REFERENCES census(tract) ON DELETE NO ACTION ON UPDATE NO ACTION
)
ENGINE = INNODB
CHARACTER SET utf8
COLLATE utf8_general_ci
ROW_FORMAT = DYNAMIC;
