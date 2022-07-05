import requests

API_url = "https://openlibrary.org"


def get_by_category(category, offset):
    target_url = API_url + "/subjects/" + category + ".json?limit=50&offset=" + str(offset)
    r = requests.get(target_url)
    return r.json()

def get_by_work(work):
    target_url = API_url + "/works/" + work + ".json"
    r = requests.get(target_url)
    return r.json()