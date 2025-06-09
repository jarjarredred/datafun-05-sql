SELECT a.name AS author_name, COUNT(b.book_id) AS book_count
FROM authors a
LEFT JOIN books b ON a.author_id = b.author_id
WHERE a.author_id = 'AUTHOR_003'
GROUP BY a.name
ORDER BY book_count DESC;