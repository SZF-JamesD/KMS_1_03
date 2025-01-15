CREATE DATABASE account_management;
USE account_management;

CREATE TABLE Customers (
    customer_id VARCHAR(4) PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(255)
);

CREATE TABLE Accounts (
    account_number VARCHAR(6) PRIMARY KEY,
    account_type VARCHAR(50),
    balance DECIMAL(10, 2),
    customer_id VARCHAR(4),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

UPDATE Accounts 
SET account_type = 'Checking', balance = 1000 
WHERE account_number = '000001' AND customer_id = '0001';

