import csv
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


URL = "https://www.goodreads.com/list/show/1.Best_Books_Ever"
OUTPUT_FILE = Path(__file__).with_name("top_books.csv")


def scrape_books():
    response = requests.get(
        URL,
        params={"page": 1},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=20,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr", itemtype="http://schema.org/Book")
    books = []

    for row in rows:
        title_tag = row.find("a", class_="bookTitle")
        author_tag = row.find("a", class_="authorName")
        rating_tag = row.find("span", class_="minirating")

        if not title_tag or not author_tag:
            continue

        title = re.sub(r"\s+", " ", title_tag.get_text()).strip()
        author = re.sub(r"\s+", " ", author_tag.get_text()).strip()
        rating = rating_tag.get_text(" ", strip=True) if rating_tag else "N/A"

        books.append({
            "Title": title,
            "Author": author,
            "Rating": rating,
        })

    return books


def main():
    try:
        books = scrape_books()

        if not books:
            print("No books found. The website layout may have changed.")
            return

        with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["Title", "Author", "Rating"],
            )
            writer.writeheader()
            writer.writerows(books)

        print(f"Saved {len(books)} books to {OUTPUT_FILE.name}")

    except requests.RequestException as error:
        print(f"Could not retrieve the page: {error}")


if __name__ == "__main__":
    main()