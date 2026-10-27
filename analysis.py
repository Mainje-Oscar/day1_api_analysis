"""
API Data Analysis Using Python Structures
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from numpy import extract
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error occured during fetch: {e}")
        return []


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    space = "  " * indent
    for key, value in record.items():
        print(f"{space}- {key}: {type(value).__name__}")
        if isinstance(value, dict):
            explore(value, indent + 1)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    flat_customers = []
    for customer in customers:
        # Extracting the tld from email
        email = customer.get("email", "")
        email_domain = email.split(".")[-1] if "." in email else ""

        row = {
            "id": customer.get("id"),
            "name": customer.get("name"),
            "username": customer.get("username"),
            "email": email,
            "email_domain": email_domain,
            "phone": customer.get("phone"),
            "city": customer.get("address", {}).get("city"),
            "zipcode": customer.get("address", {}).get("zipcode"),
            "latitude": float(customer.get("address", {}).get("geo", {}).get("lat", 0.0)),
            "longitude": float(customer.get("address", {}).get("geo", {}).get("lng", 0.0)),
            "company": customer.get("company", {}).get("name"),
            "website": customer.get("website")                                                                      
        }
        flat_customers.append(row)
    return flat_customers


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {customer["city"] for customer in customers if "city" in customer}


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}
    for customer in customers:
        city = customer["city"]
        counts[city] = counts.get(city, 0) + 1
    # Sort by customer count (descending)
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))    


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    domains = [customer["email_domain"] for customer in customers if customer.get("email_domain")]
    unique_domains = set(domains)
    counts = {domain: domains.count(domain) for domain in unique_domains}
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))



def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert to DataFrame, rename id column to customer_id"""
    df = pd.DataFrame(rows)
    df = df.rename(columns={"id": "customer_id"})
    return df

def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 5))
    cities = list(counts.keys())
    values = list(counts.values())

    plt.bar(cities, values)
    plt.title("Customers by City", fontsize=14)
    plt.xlabel("City", fontsize=12)
    plt.ylabel("Number of Customers", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()



if __name__ == "__main__":
    # Creating output folder
    output = Path("output")
    output.mkdir(exist_ok=True)

    print("~~~ Step 1 and 2: Fetching and exploring data ~~~")
    data = get_customers()
    if data:
        print(f"Sample structuer of customer records:")
        explore(data[0])

        print("\n~~~ Step 3: Flattened customer attributes ~~~")
        rows = extract_attributes(data)

        print("\n~~~ Step 4: Unique cities ~~~")
        cities = unique_cities(rows)
        print(f"Customers found: {len(rows)}")
        print(f"Unique cities  : {len(cities)}")
        # Marketing insight
        print("Insight: Each customer lives in a unique city, " \
        "there is no concentration in any particular city")

        print("\n~~~ Counting using python ~~~")
        counts_city = city_counts(rows)
        counts_domains = email_domain_counts(rows)

        most_common_city = list(counts_city.keys())[0]
        most_common_value = list(counts_city.values())[0]
        print(f"Most common city: {most_common_city} ({most_common_value})")
        print(f"Email domains   : {counts_domains}")

        print("\n~~~ Confirming using Pandas ~~~")
        df_customers = to_dataframe(rows)
        print(f"Shape: {df_customers.shape}")
        print("\nData types:")
        print(df_customers.dtypes)

        print("\n~~~ Step 7 Exporting CSVs ~~~")
        # Customers
        df_customers.to_csv(output/"customer.csv", index=False)

        # City counts 
        df_city_counts = pd.DataFrame(list(counts_city.items()), columns=["city", "customer_count"])
        df_city_counts.to_csv(output/"city_counts.csv", index=False)
        print("CSVs generated in output folder.")

        print("\n~~~ Visualizing customer distribution ~~~")
        plot_distribution(counts_city, output/"customer_distribution.png")
        print(f"Chart saved to: {output/'customer_distribution.png'}")
        
        # A more informative secondary chart
        plt.figure(figsize=(10, 5))
        plt.bar(list(counts_domains.keys()), list(counts_domains.values()))
        plt.title("Customer distribution by email TLD", fontsize=14)
        plt.xlabel("Email Domain Extension", fontsize=12)
        plt.ylabel("Number of Customers", fontsize=12)
        plt.tight_layout()
        plt.savefig(output/"domain_distribution.png")
        plt.close()
