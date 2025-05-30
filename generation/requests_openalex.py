import requests
import pandas as pd
import requests
import pandas as pd
import requests
import pandas as pd

def get_author_works(author_name, max_results=100):
    url = "https://api.openalex.org/authors"
    params = {"search": author_name}
    response = requests.get(url, params=params)
    data = response.json()
    
    if not data["results"]:
        return None
    
    author = data["results"][0]
    author_id = author["id"]
    print(f"Found Author: {author['display_name']} : {author_id}")
    
    works_url = "https://api.openalex.org/works"
    works_params = {
        "filter": f"author.id:{author_id}",
        "per_page": max_results,
        "sort": "cited_by_count:desc"
    }
    
    works_response = requests.get(works_url, params=works_params)
    works_data = works_response.json()
    
    works_list = []
    for work in works_data.get("results", []):
        primary_location = work.get("primary_location")
        journal = 'N/A'
        
        if primary_location:
            source = primary_location.get('source')
            if source:
                journal = source.get('display_name', 'N/A')
        
        works_list.append({
            "title": work.get('title', 'N/A'),
            "year": work.get('publication_year', 'N/A'),
            "journal": journal,
            "doi": work.get('doi', 'N/A'),
            "cited_by_count": work.get('cited_by_count', 0)
        })
    
    df = pd.DataFrame(works_list)
    
    if df.empty:
        print("No works found for this author.")
        return pd.DataFrame()
    
    df_filtered = df[
        (df['doi'] != 'N/A') & 
        (df['journal'] != 'N/A') & 
        (df['cited_by_count'] > 0)
    ].copy()  
    
    if not df_filtered.empty:
        df_filtered['person'] = author_name
    
    return df_filtered
