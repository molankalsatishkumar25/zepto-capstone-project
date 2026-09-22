# Module 1 - Zepto Data Pipeline

## Objective

Build a reusable data pipeline that scrapes book data from Books to Scrape, cleans and enriches the data, stores it in a normalized SQLite database, and validates the data using SQL and pandas.

## Source

Website: https://books.toscrape.com/

The pipeline scrapes the first 5 paginated listing pages.

- Pages scraped: 1-5
- Books collected: 100
- Categories found: 29

## Data Collected

The following fields are collected from the source:

- `title`
- `price`
- `rating`
- `availability`
- `category`

The cleaned dataset contains:

- `title`
- `price_gbp`
- `rating`
- `in_stock`
- `category`
- `price_inr`

## Cleaning and Transformation

### Price

The source price is stored as text and may contain encoded pound symbols such as `Â£`.

The pipeline removes the currency symbol and converts the value to a numeric `float`.

Final column:

`price_gbp`

### Rating

The source rating is represented as text:

- One → 1
- Two → 2
- Three → 3
- Four → 4
- Five → 5

Final column:

`rating`

The final rating values are integers from 1 to 5.

### Availability

The source availability text is converted into a boolean value.

- `In stock` → `True`
- Other availability text → `False`

Final column:

`in_stock`

### Parsing Failures

Numeric parsing uses defensive conversion with `errors="coerce"`.

If numeric parsing failures occur:

- Numeric price values are median-imputed.
- Rating values are median-imputed and converted to integers.

For the current 100-book dataset:

- Price parsing failures: 0
- Rating parsing failures: 0

Therefore, no imputation was required for the current dataset.

### Missing Values and Duplicates

The final validation confirmed:

- Missing `price_gbp`: 0
- Missing `rating`: 0
- Missing `price_inr`: 0
- Duplicate rows: 0

## Currency Conversion

The project-defined fixed conversion rate is:

**1 GBP = 105.50 INR**

This is an artificial project rate and is not retrieved from a live currency API.

The INR price is calculated as:

`price_inr = price_gbp × 105.50`

The final validation confirmed that all `price_inr` values were calculated using this exact rate.

## SQLite Database

The pipeline creates:

`data/zepto_books.db`

The database contains two normalized tables:

### categories

- `category_id` - Primary Key
- `category_name` - Unique category name

### books

- `book_id` - Primary Key
- `title`
- `price_gbp`
- `price_inr`
- `rating`
- `in_stock`
- `category_id` - Foreign Key referencing `categories`

Foreign-key validation completed successfully with zero violations.

## SQL Queries

Five SQL queries are included in:

`sql/queries.sql`

The query outputs are saved in:

`sql/query_outputs.md`

The queries demonstrate:

- SELECT and WHERE
- ORDER BY
- LIMIT
- DISTINCT
- BETWEEN
- IN
- JOIN

Query results were read using `pandas.read_sql()`.

## SQL JOIN and Pandas Merge

The SQL JOIN between `books` and `categories` was reproduced using:

`pandas.merge()`

The final validation confirmed:

- SQL JOIN rows: 10
- Pandas merge rows: 10
- SQL JOIN and pandas merge match: True

## Project Files

```text
data_pipeline/
├── data/
│   └── zepto_books.db
├── notebooks/
│   └── 01_zepto_data_pipeline.ipynb
├── sql/
│   ├── queries.sql
│   └── query_outputs.md
└── README.md