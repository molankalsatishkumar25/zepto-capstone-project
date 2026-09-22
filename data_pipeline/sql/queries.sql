-- Query 1: Books priced above £40, ordered by highest price
SELECT
    title,
    price_gbp,
    price_inr,
    rating
FROM books
WHERE price_gbp > 40
ORDER BY price_gbp DESC
LIMIT 10;


-- Query 2: List all distinct book categories
SELECT DISTINCT category_name
FROM categories
ORDER BY category_name;


-- Query 3: Books priced between £20 and £40
SELECT
    title,
    price_gbp,
    price_inr,
    rating
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp ASC;


-- Query 4: Top-rated books with their category names
SELECT
    b.title,
    c.category_name,
    b.price_gbp,
    b.price_inr,
    b.rating
FROM books AS b
JOIN categories AS c
    ON b.category_id = c.category_id
ORDER BY b.rating DESC, b.price_gbp DESC
LIMIT 10;


-- Query 5: Books from selected categories
SELECT
    b.title,
    c.category_name,
    b.price_gbp,
    b.rating
FROM books AS b
JOIN categories AS c
    ON b.category_id = c.category_id
WHERE c.category_name IN ('Poetry', 'Mystery', 'History')
ORDER BY b.price_gbp DESC;
