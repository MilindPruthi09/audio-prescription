import requests

def disease_result(disease):
    endpoint = "https://disease-infosearch.nlm.nih.gov/api/search"
    params = {"name": disease, "size": 1}

    response = requests.get(endpoint, params=params)

    if response.status_code == requests.codes.ok:
        data = response.json()
        description = data['results'][0]['description']
        return(description)
    else:
        return("Failed to retrieve the disease description.")