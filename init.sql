-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS testdb;

-- Switch to the created database
USE testdb;

-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);
