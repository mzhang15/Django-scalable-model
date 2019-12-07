/* Create our database */
CREATE DATABASE app CHARACTER SET utf8;
/* Setup permissions for the server */
CREATE USER 'appserver'@'localhost' IDENTIFIED BY 'foobarzoot';
CREATE USER 'www-data'@'localhost' IDENTIFIED BY 'foobarzoot';
GRANT ALL ON app.* TO 'appserver'@'localhost';
GRANT ALL ON app.* TO 'www-data'@'localhost';
/* Permissions for using Docker DBs */
CREATE USER 'appserver'@'172.17.0.1' IDENTIFIED BY 'foobarzoot';
GRANT ALL ON app.* TO 'appserver'@'172.17.0.1';
