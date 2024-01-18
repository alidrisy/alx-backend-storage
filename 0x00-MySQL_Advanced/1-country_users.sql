-- creates a table users withe id, email, name and country rows

CREATE TABLE IF NOT EXISTS users (
	id INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country ENUM("US", "CO", "TN") DEFAULT "US"
	);
