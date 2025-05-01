# MySQL Database Best Practices Guide

This repository contains guidance, examples, and best practices for working with MySQL databases. The following topics are covered in detail:

- Creating Tables with Constraints
- Optimizing Queries with Indexes
- Stored Procedures and Functions
- Views
- Triggers

## Table of Contents

- [Creating Tables with Constraints](#creating-tables-with-constraints)
- [Optimizing Queries with Indexes](#optimizing-queries-with-indexes)
- [Stored Procedures and Functions](#stored-procedures-and-functions)
- [Views in MySQL](#views-in-mysql)
- [Triggers in MySQL](#triggers-in-mysql)
- [Examples](#examples)
- [Best Practices](#best-practices)

## Creating Tables with Constraints

Constraints are rules enforced on data columns in tables to ensure data integrity and accuracy. MySQL supports the following constraints:

### PRIMARY KEY

The PRIMARY KEY constraint uniquely identifies each record in a table. It must contain UNIQUE values and cannot be NULL.

```sql
CREATE TABLE employees (
    employee_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (employee_id)
);
```

### FOREIGN KEY

The FOREIGN KEY constraint is used to link two tables together and prevent actions that would destroy links between tables.

```sql
CREATE TABLE orders (
    order_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

### UNIQUE

The UNIQUE constraint ensures that all values in a column are different.

```sql
CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (user_id),
    UNIQUE (username),
    UNIQUE (email)
);
```

### CHECK

The CHECK constraint ensures that values in a column satisfy a specific condition.

```sql
CREATE TABLE products (
    product_id INT NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (product_id),
    CHECK (price > 0)
);
```

### NOT NULL

The NOT NULL constraint ensures that a column cannot have NULL values.

```sql
CREATE TABLE contacts (
    contact_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    PRIMARY KEY (contact_id)
);
```

### DEFAULT

The DEFAULT constraint provides a default value for a column when no value is specified.

```sql
CREATE TABLE orders (
    order_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL DEFAULT CURRENT_DATE(),
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    PRIMARY KEY (order_id)
);
```

## Optimizing Queries with Indexes

Indexes are special lookup tables that the database search engine can use to speed up data retrieval. They are similar to a book's index.

### Types of Indexes

#### Basic Index

```sql
CREATE INDEX idx_lastname ON employees(last_name);
```

#### Unique Index

```sql
CREATE UNIQUE INDEX idx_email ON users(email);
```

#### Composite Index (Multi-column)

```sql
CREATE INDEX idx_name ON customers(last_name, first_name);
```

#### Full-Text Index

```sql
CREATE FULLTEXT INDEX idx_description ON products(description);
```

### When to Use Indexes

- Columns frequently used in WHERE clauses
- Columns used in JOIN operations
- Columns used in ORDER BY or GROUP BY clauses

### Index Best Practices

- Don't over-index tables (increases INSERT/UPDATE/DELETE time)
- Regularly analyze query performance with EXPLAIN
- Consider column cardinality (number of distinct values)
- Periodically review and optimize indexes
- Be mindful of index size in memory

## Stored Procedures and Functions

### Stored Procedures

Stored procedures are prepared SQL code that can be saved and reused. They accept parameters and can perform complex operations.

#### Basic Stored Procedure

```sql
DELIMITER //
CREATE PROCEDURE GetAllCustomers()
BEGIN
    SELECT * FROM customers;
END //
DELIMITER ;

-- Call the procedure
CALL GetAllCustomers();
```

#### Stored Procedure with Parameters

```sql
DELIMITER //
CREATE PROCEDURE GetCustomerOrders(IN customerId INT)
BEGIN
    SELECT * FROM orders WHERE customer_id = customerId;
END //
DELIMITER ;

-- Call the procedure
CALL GetCustomerOrders(123);
```

#### Stored Procedure with Output Parameters

```sql
DELIMITER //
CREATE PROCEDURE GetOrderStatistics(
    IN orderYear INT,
    OUT totalOrders INT,
    OUT totalValue DECIMAL(12,2)
)
BEGIN
    SELECT COUNT(*), SUM(total_amount)
    INTO totalOrders, totalValue
    FROM orders
    WHERE YEAR(order_date) = orderYear;
END //
DELIMITER ;

-- Call the procedure
CALL GetOrderStatistics(2023, @total, @value);
SELECT @total, @value;
```

### Functions

Functions are similar to procedures but must return a single value and can be used directly in SQL statements.

```sql
DELIMITER //
CREATE FUNCTION CalculateTotal(price DECIMAL(10,2), quantity INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10,2);
    SET total = price * quantity;
    RETURN total;
END //
DELIMITER ;

-- Use the function
SELECT product_name, price, quantity, CalculateTotal(price, quantity) AS total_price
FROM order_items;
```

## Views in MySQL

Views are virtual tables based on the result of SQL statements. They don't store data but provide a way to simplify complex queries and restrict access to data.

### Creating a View

```sql
CREATE VIEW customer_orders AS
SELECT c.customer_id, c.name, o.order_id, o.order_date, o.total_amount
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- Query the view
SELECT * FROM customer_orders WHERE total_amount > 1000;
```

### Updatable Views

Simple views can be updated to affect the underlying tables:

```sql
CREATE VIEW active_customers AS
SELECT * FROM customers WHERE status = 'active';

-- This can update the underlying table
UPDATE active_customers SET credit_limit = 5000 WHERE customer_id = 101;
```

### WITH CHECK OPTION

Prevents updates that would make rows invisible to the view:

```sql
CREATE VIEW high_value_products AS
SELECT * FROM products WHERE price > 1000
WITH CHECK OPTION;

-- This would fail as it would make the product invisible to the view
UPDATE high_value_products SET price = 500 WHERE product_id = 10;
```

### View Benefits

- Simplifies complex queries
- Provides an additional security layer
- Enables backward compatibility when schema changes
- Presents data in a format specific to different users

## Triggers in MySQL

Triggers are SQL code that automatically execute in response to events (INSERT, UPDATE, DELETE) on a table.

### Types of Triggers

- BEFORE INSERT/UPDATE/DELETE: Execute before the operation
- AFTER INSERT/UPDATE/DELETE: Execute after the operation

### Creating a Trigger

```sql
DELIMITER //
CREATE TRIGGER before_employee_update
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    IF NEW.salary < OLD.salary THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Salary cannot be reduced';
    END IF;
END //
DELIMITER ;
```

### Audit Trail Example

```sql
DELIMITER //
CREATE TRIGGER after_product_update
AFTER UPDATE ON products
FOR EACH ROW
BEGIN
    INSERT INTO product_audit_log (product_id, old_price, new_price, change_date)
    VALUES (NEW.product_id, OLD.price, NEW.price, NOW());
END //
DELIMITER ;
```

### Common Uses for Triggers

- Enforcing complex business rules
- Audit logging
- Automatically updating related tables
- Validation before data modifications
- Maintaining denormalized data for reporting

## Examples

This repository includes practical examples for all the topics covered:

- `/examples/constraints/` - Examples of different constraint implementations
- `/examples/indexes/` - Index creation and performance comparison
- `/examples/procedures/` - Various stored procedure examples
- `/examples/functions/` - MySQL function examples
- `/examples/views/` - Different types of views
- `/examples/triggers/` - Trigger examples for different scenarios

## Best Practices

### Database Design
- Normalize your database to reduce redundancy
- Use appropriate data types for columns
- Always define a primary key for each table
- Use meaningful naming conventions

### Performance
- Create indexes on columns frequently used in WHERE, JOIN, ORDER BY clauses
- Use EXPLAIN to analyze query performance
- Avoid using SELECT * in production code
- Break complex queries into smaller, more manageable pieces

### Security
- Use prepared statements to prevent SQL injection
- Grant minimum necessary privileges to users
- Encrypt sensitive data
- Implement row-level security where needed

### Maintenance
- Regularly backup your database
- Schedule routine maintenance tasks
- Monitor performance and optimize as needed
- Keep MySQL updated with security patches

## License

This project is licensed under the MIT License - see the LICENSE file for details.
