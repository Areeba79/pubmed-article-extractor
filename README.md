# PubMed Article Extractor

This project fetches and cleans PubMed articles using the NCBI E-utilities API.

## 🔍 Task Description
- Query: **oncology biomarkers**
- Articles fetched: **50**
- Data source: **NCBI PubMed**
- Output format: **JSON**

## 📦 Extracted Fields
- PMID
- Title
- Authors
- Abstract
- Publication date
- Journal

## 🛠️ Technologies Used
- Python 3
- NCBI E-utilities API
- requests
- XML parsing

## 🚀 How to Run

```bash
pip install -r requirements.txt
python src/pubmed_extractor.py

📁 Output

The cleaned articles are saved as:
output/pubmed_oncology_biomarkers.json

📝 Notes

PubMed may return withdrawn or incomplete records.
The pipeline fetches extra PMIDs internally and caps the final output at exactly 50 clean articles, as required.