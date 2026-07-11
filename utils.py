from typing import Any
import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_FR_full_text(
    df: pd.DataFrame,
    doc_num: str,
    date: str,
) -> str:
    """
    Fetches document full text in .xml format.
    """
    full_text_url = (
        f"https://www.federalregister.gov/documents/full_text/xml/{date}/{doc_num}.xml"
    )
    response = requests.get(full_text_url)
    return response.text


def get_FR_full_text_formatted(url: str) -> str:
    """
    Fetches a single Federal Register document, parses the XML,
    and concatenates text from all <FP> tags.
    """
    response = requests.get(url)
    doc_xml = response.text
    soup = BeautifulSoup(doc_xml, features="xml")
    fp_tags = soup.find_all("FP")
    print(fp_tags)

    clean_text = " ".join(tag.get_text(strip=True) for tag in fp_tags)
    return clean_text


def define_date_range(num_days: int) -> str:
    """
    Returns a YYYY-MM-DD string for the specified number of days
    before today's date.
    """
    time_period = (
        datetime.date.today() - datetime.timedelta(days=num_days)
    ).isoformat()
    print(f"Defined as {time_period}.")
    return time_period


def fetch_FR(
    url: str,
    fields: list[str],
    publication_date_gte: str,
    per_page: int = 1000,
    max_pages: int | None = None,
) -> list[dict[str, Any]]:
    """
    Fetch Federal Register documents published on or after a given date.
    Supports pagination to retrieve all results.

    Args:
        url: The API endpoint URL.
        fields: List of fields to retrieve.
        publication_date_gte: Start date for filtering (YYYY-MM-DD format).
        per_page: Number of results per page (default: 1000).
        max_pages: Maximum number of pages to fetch. None fetches all pages.

    Returns:
        A list of document dictionaries from all pages.
    """
    all_results = []
    page = 1

    try:
        while True:
            params = {
                "fields[]": fields,
                "conditions[type][]": ["RULE", "PRORULE", "PRESDOCU"],
                "conditions[publication_date][gte]": publication_date_gte,
                "per_page": per_page,
                "page": page,
            }

            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])

            if not results:
                break

            all_results.extend(results)
            print(f"Fetched page {page}: {len(results)} results")

            if max_pages and page >= max_pages:
                break

            page += 1

        print(f"Total results fetched: {len(all_results)}")
        return all_results

    except requests.RequestException as e:
        print(f"Error fetching Federal Register data: {e}")
        return all_results