-- Add a new column to the author table to store the amount of books the author has published
ALTER TABLE authors ADD COLUMN author_number_of_books INT;

-- Update the author_number_of_books column in the author table
UPDATE authors
SET author_number_of_books = (
    SELECT publication_year - birth_year
    FROM authors
    WHERE authors.author_id = books.author_id
);