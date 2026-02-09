# template_scraping/src/helpers/utils.py
import csv
import selectolax


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
