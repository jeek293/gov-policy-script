# **Federal Policy Tracker: NLP-Driven Sector Analysis POC**

## **Project Overview**
This analytical tool provides a pipeline for monitoring US Federal Government activity. It identifies relevant policy changes by comparing real-time Federal Register documents against specific industry profiles using transformer-based semantic similarity. Although fairly simple, this is much more so meant to demonstrate driving business value, rather than technical grace.

### **Technical Workflow**
1.  **ETL Pipeline**: Extracts the last 6 months of rules and presidential documents from the `FederalRegister.gov` API.
2.  **Data Munging**: Filters out noise (e.g., 'Notices') and handles high-sparsity data (99% null thresholding).
3.  **Content Retrieval**: Implements an XML-scraping engine to fetch full-text documents with rate-limiting best practices.
4.  **Semantic Analysis**: Utilizes Bi-Encoder to compute similarity scores between specific industry keywords (e.g., Cybersecurity, AI, Biotech) and government text.

### **Business Value**
Enables policy analysts and tech executives to programmatically identify regulatory signals within thousands of daily government publications that might otherwise be missed by keyword-only searches.

### **TODOS**:
- Clean up output
- Add Vector DB for storage, metadata for efficient and precise retrieval
- Add LLM API calls for additional analysis 
- Integrate other data sources - ECR, Regulations.gov, etc
- add pagination for FR calls
- Find solution for updated docs
