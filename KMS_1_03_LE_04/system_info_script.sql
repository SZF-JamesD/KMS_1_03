CREATE DATABASE system_analysis;
USE system_analysis;

CREATE TABLE system_info (
    id 	INTEGER PRIMARY KEY AUTO_INCREMENT,
    analysis_time DATETIME,
    os_name VARCHAR(255),
    os_version varchar(255),
    os_release varchar(255),
    architecture varchar(50),
    python_version varchar(50),
    machine varchar(100),
    processor varchar(255),
    node varchar(255),
    python_path text
);