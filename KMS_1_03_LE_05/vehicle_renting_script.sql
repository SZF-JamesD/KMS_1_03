CREATE DATABASE vehicle_rental_management;
USE vehicle_rental_management;

CREATE TABLE vehicle_info (
    vehicle_id 	INT AUTO_INCREMENT PRIMARY KEY,
	brand VARCHAR(255),
	model VARCHAR(255),
	reg_no VARCHAR(15),
	vehicle_status ENUM('available', 'rented', 'maintenance') DEFAULT 'available'
);

CREATE TABLE customer_info (
	customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name varchar(255),
	telephone_number VARCHAR(255),
	email VARCHAR(255),
	payment_choice ENUM('card', 'cash') DEFAULT 'card'
);

CREATE TABLE rental_history(
	rental_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    customer_id INT NOT NULL,
    rental_start DATETIME NOT NULL,
    rental_end DATETIME,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle_info(vehicle_id),
    FOREIGN KEY (customer_id) REFERENCES customer_info(customer_id)
);

INSERT INTO vehicle_info (brand, model, reg_no, vehicle_status) VALUES
('Toyota', 'Corolla', 'AB123CD', 'available'),
('Honda', 'Civic', 'XY456ZT', 'rented'),
('BMW', '3 Series', 'JK789LM', 'maintenance'),
('Ford', 'Focus', 'LM012NP', 'available'),
('Audi', 'A4', 'OP345QR', 'rented');

INSERT INTO customer_info (customer_name, telephone_number, email, payment_choice) VALUES
('John Doe', '555-1234', 'john.doe@example.com', 'card'),
('Jane Smith', '555-5678', 'jane.smith@example.com', 'cash'),
('Alice Brown', '555-8765', 'alice.brown@example.com', 'card'),
('Bob White', '555-4321', 'bob.white@example.com', 'card'),
('Charlie Green', '555-6789', 'charlie.green@example.com', 'cash');

INSERT INTO rental_history (vehicle_id, customer_id, rental_start, rental_end) VALUES
(1, 1, '2024-01-01', '2024-01-05'),
(2, 2, '2024-01-10', '2024-01-15'),
(3, 3, '2024-01-20', '2024-01-22'),
(4, 4, '2024-02-01', '2024-02-05'),
(5, 5, '2024-02-10', '2024-02-15');
