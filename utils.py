import requests
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm.auto import tqdm

def get_FR_full_text(df, doc_num, date):
  """
  Fetches document full text in .xml format
  """
  full_text_url = f'https://www.federalregister.gov/documents/full_text/xml/{date}/{doc_num}.xml'
  response = requests.get(full_text_url)
  return response.text

def get_FR_full_text_formatted(url):
  """
  Fetches singular FR doc, returns as xml, and parses Federal Register XML and concatenates text from all <FP> tags: FP indicates the actual text
  """
  response = requests.get(url)
  doc_xml =  response.text
  soup = BeautifulSoup(doc_xml, features='xml')
  fp_tags = soup.find_all('FP')
  print(fp_tags)
  # Extract text from each tag and join with spaces
  clean_text = " ".join([tag.get_text(strip=True) for tag in fp_tags])
  return clean_text

def define_date_range(num_days):
    """
    Returns YYYY-MM-DD string for the num_days number of days before today's date
    """
    time_period = (
        datetime.date.today() - datetime.timedelta(days=num_days)
    ).isoformat()
    print(f"Defined as {time_period}.")
    return time_period

def fetch_FR(url, fields, publication_date_gte, per_page=1000):
    """
    Fetch Federal Register documents published on or after a given date.
    Returns the list of document dictionaries.
    """

    params = {
        "fields[]": fields,
        "conditions[type][]": ["RULE", "PRORULE", "PRESDOCU"],
        "conditions[publication_date][gte]": publication_date_gte,
        "per_page": per_page,
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()["results"]

    except requests.RequestException as e:
        print(f"Error fetching Federal Register data: {e}")
        return []
