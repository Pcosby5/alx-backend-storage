-- add a new attribute (country), using the ALTER TABLE
-- to alter the users table

ALTER TABLE users
ADD COLUMN country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US';
