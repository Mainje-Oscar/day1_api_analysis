# Day 1: API Data Analysis Using Python Structures

This project is a data analysis pipeline developed for **Pesa Pulse**, a Nairobi-based fintech start-up. 
It pulls customer profile data from an API, explores its structure, flattens various fields in the data, 
performs customer distribution counts, and exports the data in csv format.

The project is managed using **uv** to ensure that it is reproducable and is implemented in an isolated environment.

## Approach taken
1. **Extraction:** Data is queried from the API with a timeout and built-in error handling via `requests` to prevent runtime crashes.
2. **Inspection:** Built with a recursive mapping functionality (`explore`) to drill down into nested JSON records without relying on hardcoded indices.
3. **Aggregations:** Analyzed customer segments first using pure Python data structures to establish references before conversion into a Pandas DataFrame.
4. **Tools used:** Used `uv` to automatically handle isolated virtual environments and eliminate manual activation steps.

## Project Structure
The data pipeline maps down several layers of dictionaries.

* `customer_record['address']` (Dictionary)
* `customer_record['address']['geo']` (Dictionary)

The deepest data point is the geographic coordinates layer. To find latitude and longitude records from the source, you go through the dictionary indices in a hierarchy as follows:

* `customer_record['address']['geo']['lat']` and `record['address']['geo']['lng']` (Deepest data attributes)

## How to run the analysis using `uv`

### Prerequisites
Ensure you have `uv` installed on your computer.

### Execution Steps
1. **Clone the repository and navigate into the project root:**
   ```bash
   cd day1-api-analysis
   ```

2. **Run the analysis pipeline:**
   ```bash
   uv run analysis.py
   ```

## Business Findings
* The analysis reveals that our count of unique cities (10)  matches the customer count (10). This means Pesa Pulse has equal geographic spread and no customer clusters. Marketing should avoid regional campaigns and focus on wider campaign targets i.e. through the digital media.
* Because every city in our data contains only one individual customer, standard city-level bar chart results in a flat distribution chart.
* Grouping data by email domains reveals some differences as there are some domains like `.biz` vs. `.tv`) that seem more popular. Thi shows that grouping by digital customer attributes will yield much better marketing cohorts than physical zip codes.

## Assumptions made
* Assumed that missing geographic entries or structural values are acceptable defaults at `0.0` or empty strings rather than completely dropping the customer record from analysis.
* Assumed standard notation format (`username@domain.tld`) for domain splitting metrics.
