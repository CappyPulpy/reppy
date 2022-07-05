import pandas as pd
import APIhandler


def get_price_df():
    url = 'https://drive.google.com/file/d/1aJUlXVvZ3WmI3sPPK5vbr0GdFOS5fnL6/view?usp=sharing'
    file_id = url.split('/')[-2]
    dwn_url = 'https://drive.google.com/uc?id=' + file_id
    df = pd.read_csv(dwn_url)
    return df


jsonlist = []


def load_to_jsonlist(category):
    offset = 0
    returned_json = APIhandler.get_by_category(category, offset)
    jsonlist.append(returned_json)
    while returned_json.get("works"):
        offset += 50
        returned_json = APIhandler.get_by_category(category, offset)
        jsonlist.append(returned_json)


def construct_df():
    frame = pd.DataFrame(
        columns=["Book ID", "Book Title", "Categories", "Authors Names", "Price", "Description", "Excerpts"])

    load_to_jsonlist("relational_databases")
    load_to_jsonlist("database_software")
    load_to_jsonlist("python")

    price_df = get_price_df()
    price_df = dict(price_df.values)
    for json in jsonlist:
        for book in json.get("works"):
            row = {
                "Book ID": book.get("key").split('/')[2],
                "Book Title": book.get("title"),
                "Categories": book.get("subject"),
                "Authors Names": [auth.get("name") for auth in book.get("authors")],  # should prettyprint
                "Description": book.get("description")
            }
            try:
                row["Price"] = price_df[row["Book ID"]]
            except KeyError:
                row["Price"] = None

            try:
                row["Excerpts"] = ';'.join([exc["excerpt"]["value"] for exc in book.get("excerpts")])
            except TypeError:
                row["Excerpts"] = None
            frame = frame.append(row, ignore_index=True)
    return frame
