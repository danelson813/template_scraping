# template_scraping/src/helpers/utils.py
import csv
import selectolax
import duckdb


def save_to_csv(results):
    keys = results[0].keys()
    with open("data/results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(results)


def gather_data(tree: selectolax.parser.HTMLParser) -> list:
    data_ = []
    # find containers
    containers = tree.css("article")
    for container in containers:
        try:
            name = container.css_first("h3 a").attrs["title"]
            price = container.css_first("p.price_color").text()[1:]
            datum = {"name": name, "price": float(price)}
            data_.append(datum)
            # print(datum)
        except Exception as e:
            print(f"Error parsing page {e}")
    return data_


def save_to_duckdb():
    conn = duckdb.connect("data/results.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS books;")
    cursor.execute("CREATE TABLE books (name text, price real)")
    cursor.sql("INSERT INTO books SELECT * FROM read_csv_auto('data/results.csv')")
    conn.commit()
    items = cursor.execute("SELECT * FROM books;").fetchall()
    print("there are {} items".format(len(items)))
    print(cursor.execute("SELECT EXISTS(SELECT 1 FROM books)").fetchall())
