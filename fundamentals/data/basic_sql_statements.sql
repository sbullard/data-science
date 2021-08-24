-- Creating a  database
-- CREATE DATABASE IF NOT EXISTS netflix;

-- Using a specific database
USE netflix;

-- Create the table movies if it does not already exist
CREATE TABLE IF NOT EXISTS movies (
                   id INT,
                   title VARCHAR(255),
                   director VARCHAR(100),
                   release_date INT,
                   runtime INT,
                   rating VARCHAR(15),
                   category VARCHAR(50));
				
-- Select all rows from a table
Select * from movies;

-- WHERE
-- WHERE statements are very similar to IF statments, however WHERE statements can only be applied
-- to existing variable values

-- WHERE exmpale counting the number of rows based on certain condition
SELECT COUNT(*) FROM movies
WHERE release_date=2018 AND rating= "TV-MA";


-- ORDER BY 
-- Used to sort resluts by a list of columns or expressions

-- ORDER BY example
-- Select all rows with conditonal value ranges in descending order by year and runtime
SELECT * FROM movies 
WHERE runtime BETWEEN 60 AND 140 
ORDER BY release_date DESC, runtime DESC;


-- DISTINCT 
-- Used to get all unique valus in a column of data (i.e. no repeat values)
-- DISTINCT example
SELECT DISTINCT(rating) FROM movies;



-- AGGREGATE FUNCTIONS
-- Functions that return a single value from a bag of tuples, AVG(), MIN(), MAX(), SUM(), COUNT()

-- This example selects avearge runtime for R rated movies
SELECT ROUND(AVG(runtime), 0)
FROM movies WHERE rating = 'R';

-- This example selects the movie with the longest runtime
SELECT  id, title, MAX(runtime)
FROM movies;



-- GROUP BY
-- Used to group rows that have the same values in to summary rows such as "find the # of customers in each country"
-- GROUP BY is often used to aggregate data by being used with functions like COUNT(), MIN/MAX(), SUM(), AVG()

-- GROUP BY example counting the total number of movies by rating
SELECT rating, COUNT(*) from movies
GROUP BY rating;

-- GROUP BY exmample only counting the R rated movies
SELECT rating, COUNT(*)
FROM movies
WHERE rating="R"
GROUP BY rating;


-- HAVING
-- Filters resulst based on aggregation computations, this is used in conjunction with GROUP BY
-- and performs similarly to the WHERE clause. Note that with both having and where are filtering 
-- functions and these have to be performed AFTER the aggreagte calculation. This makes sense
SELECT rating, COUNT(*)
FROM movies
GROUP BY rating
HAVING rating = 'R';



-- JOINS

-- Join clauses are used to combine rows from two or more tables based on related columns between them

-- There are 4 types of joins in SQL

-- JOIN (a cross join) - returns all the rows of the first table with all additional rows from the second (that aren't in the first)
-- INNER JOIN - returns rows that have matching values in BOTH tables

-- OUTER JOINS (LEFT & RIGHT) -returnsall records where there is a match in either the left or right tables
-- LEFT JOIN - return all rows from the left table and the matched records from the right
-- RIGHT JOIN - retuns all records from the right table, and the matched records from the left
-- IMPORTANT NOTE: When no match is found null or none values will be entered (therefore all rows will be returned

-- JOIN example simply combining the two tables together where region code = 8
SELECT movies.title, movies.release_date, movies.rating, region.region_code
FROM movies
JOIN region
ON region.id = movies.id
WHERE region_code = 8;

-- INNER JOIN example combining the tables only where id matches in both tables (in this case id's match exactly
SELECT movies.title, movies.release_date, movies.rating, region.region_code
FROM movies
INNER JOIN region
ON region.id = movies.id;

-- LEFT (OUTER) JOIN example which includes all the values from the left table regardless of match
-- in this examlpe all the rows match, so the entire table is returned with no nulls, however if there were
-- different id's in the region table, then those values would have been returned as Null
SELECT movies.title, movies.release_date, movies.rating, region.region_code
FROM movies
LEFT JOIN region
ON region.id = movies.id;


-- STRING FUNCTIONS
-- There are 3 ways to concat strings in SQL, ||, +, and CONCAT()

-- LIKE
-- Used for string matching (a very simple sql regex type of syntax)
-- see this link for details: https://www.w3schools.com/sql/sql_like.asp

-- Common SQL String functions: UPPER(), LOWER(), SUSBSTRING(), LENGHT(), ect. 
-- This link has a complete list with expanations: https://www.geeksforgeeks.org/sql-string-functions/



-- DATE/TIME FUNCTIONS

-- Select Currnet Time
SELECT NOW();
SELECT CURRENT_TIMESTAMP();

-- Select Current day of month
SELECT EXTRACT(DAY FROM NOW());

-- Select # of days from another date (here a 6 day difference)
-- SELECT DATEDIFF(DATE('2021-08-23'), DATE('2021-08-17')) AS days;
   
   
-- LIMIT
-- Limits the number of rows returned, good for getting top 5

-- This LIMIT example pulls all the 'TV-14' movies, sorts them by runtime and keeps the top 5
SELECT * FROM movies
WHERE rating = 'TV-14'
ORDER BY runtime DESC
LIMIT 5;


-- MORE ADVANCED STUFF

-- Output redirection - Store query reults in another table:
-- Table must not already be defined
-- table will have the same number of columns with the same types of inputs



-- NESTED QUERIES
-- Queries containing other queries (often difficult to optimize)
-- Inner queries can appear (almost) anywhere in a query
-- Nested queries are essentially joins, but more complicated (therefore, use joins if possible)

-- There are 4 main nested query functions:
-- ALL(), must satisfy expression for all rows in a sub-query
-- ANY(), must satisfy expression for at least one row in sub-query
-- IN (equivalent to ANY())
-- EXISTS - at least one row is returned

-- Nested query that pulls the title of the movies where region is 10 (note region column is not added in results)
-- THIS DOES NOT WORK AS IS, MUST ADJUST PERMISSION OR SOMETHING (JUST USE A JOIN)
SELECT title from movies
WHERE id IN (SELECT id FROM region WHERE region = 4);
-- WHERE id ANY (SELECT id FROM region WHERE region = 10);  NOTE: THIS IS THE SAME AS IN() above



-- WINDOW FUNTIONS (DIAL)
-- Perform a calculation across a set of tuples that relate to a single row
-- Like an aggregation but tuples are not grouped into single output tables
-- Window functions have 2 parts, the aggregation function then the OVER() function which is just like GROUP BY
-- PARTITION BY and ORDER BY can be used inside of OVER() to specify specific group
-- There are a few special windwo functions including ROW_NUMBER() and RANK()

-- This window function takes the top 10 


-- TRANSACTIONS
-- STORED PROCEDURES (difference between these and functions)





