"""
PubMed Article Extractor
-----------------------
Fetches PubMed articles using the NCBI E-utilities API, cleans the metadata,
and stores exactly 50 oncology biomarker articles in JSON format.

Author: Areeba Naeem
"""

import requests
import json
import xml.etree.ElementTree as ET

# =============================
# CONFIGURATION
# =============================

# Search query
QUERY = "oncology biomarkers"

# Fetch extra PMIDs to compensate for withdrawn / incomplete records
RETMAX = 70

# Email is recommended by NCBI for API usage
EMAIL = "areebasaifi6844@gmail.com"

# Output file
OUTPUT_FILE = "pubmed_oncology_biomarkers.json"

# Base URL for NCBI E-utilities
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


# =============================
# STEP 1: FETCH PMIDs (ESearch)
# =============================
def fetch_pmids(query, retmax):
    """
    Uses the ESearch endpoint to retrieve PubMed IDs (PMIDs)
    matching the given query.
    """
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": retmax,
        "retmode": "json",
        "email": EMAIL
    }

    response = requests.get(
        BASE_URL + "esearch.fcgi",
        params=params,
        timeout=30
    )
    response.raise_for_status()

    return response.json()["esearchresult"]["idlist"]


# =============================
# STEP 2: FETCH ARTICLE DETAILS
# =============================
def fetch_article_details(pmids):
    """
    Uses the EFetch endpoint to retrieve detailed article
    metadata in XML format for the given PMIDs.
    """
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
        "email": EMAIL
    }

    response = requests.get(
        BASE_URL + "efetch.fcgi",
        params=params,
        timeout=30
    )
    response.raise_for_status()

    return response.text


# =============================
# STEP 3: PARSE AND CLEAN XML
# =============================
def parse_articles(xml_data):
    """
    Parses the XML returned by PubMed and extracts
    cleaned metadata fields for each article.
    """
    root = ET.fromstring(xml_data)
    articles = []

    for article in root.findall(".//PubmedArticle"):

        # PMID
        pmid = article.findtext(".//PMID")

        # Article title
        title = article.findtext(".//ArticleTitle")
        title = title.strip() if title else None

        # Abstract (may have multiple sections)
        abstract_sections = article.findall(".//AbstractText")
        abstract = " ".join(
            section.text for section in abstract_sections if section.text
        ) if abstract_sections else None

        # Journal name
        journal = article.findtext(".//Journal/Title")

        # Publication date (best-effort)
        year = article.findtext(".//PubDate/Year")
        month = article.findtext(".//PubDate/Month")
        day = article.findtext(".//PubDate/Day")

        publication_date = None
        if year:
            publication_date = year
            if month:
                publication_date += f"-{month}"
            if day:
                publication_date += f"-{day}"

        # Author list
        authors = []
        for author in article.findall(".//Author"):
            first = author.findtext("ForeName")
            last = author.findtext("LastName")
            if first and last:
                authors.append(f"{first} {last}")

        articles.append({
            "pmid": pmid,
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "publication_date": publication_date,
            "journal": journal
        })

    return articles


# =============================
# MAIN PIPELINE
# =============================
def main():
    print("Fetching PMIDs...")
    pmids = fetch_pmids(QUERY, RETMAX)
    print(f"PMIDs retrieved: {len(pmids)}")

    print("Fetching article metadata...")
    xml_data = fetch_article_details(pmids)

    print("Parsing and cleaning articles...")
    articles = parse_articles(xml_data)

    # Enforce exactly 50 articles as required by the task
    articles = articles[:50]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)

    print(f" Saved {len(articles)} articles to '{OUTPUT_FILE}'")


# =============================
# ENTRY POINT
# =============================
if __name__ == "__main__":
    main()
