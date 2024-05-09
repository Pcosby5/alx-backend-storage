-- Drop the existing 'name' column
ALTER TABLE names DROP COLUMN name;

-- Add the new 'name' column
ALTER TABLE names ADD COLUMN name VARCHAR(255);

-- Add a generated column to store the first letter of the name
ALTER TABLE names ADD COLUMN first_letter CHAR(1) GENERATED ALWAYS AS (LEFT(name, 1)) STORED;

-- Create the index idx_name_first
CREATE INDEX idx_name_first ON names (first_letter);
