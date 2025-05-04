-- Create a composite index on names table, first character of name column and 
-- the score column
CREATE INDEX idx_name_first_score
ON names (name(1), score);
