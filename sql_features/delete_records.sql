-- Delete author only if they have this specific book
DELETE FROM authors
WHERE author_id = 'AUTHOR_003'
AND EXISTS (
    SELECT 1 FROM books 
    WHERE books.author_id = authors.author_id
    AND book_id = 'BOOK_005'
);

-- Then delete the book
DELETE FROM books 
WHERE book_id = 'BOOK_005';