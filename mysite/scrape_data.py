from serpapi import GoogleSearch
import requests
from bs4 import BeautifulSoup
import re
import os


def get_links(query):
    params = {
        "engine": "google",
        "q": query,
        "api_key": "ef0cde09a647",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]

    links = []
    for data in organic_results:
        site_link = data["link"]

        if len(links) < 5:
            links.append(site_link)

    return links


def preprocess_data(data):
    # Remove leading and trailing spaces
    cleaned_data = data.strip()
    # Remove extra spaces and junk characters using regular expression
    cleaned_data = re.sub(r"\s\s+", " ", cleaned_data)
    cleaned_data = re.sub(r"\W+", " ", cleaned_data)

    return cleaned_data


def scrape_and_store(
    link,
    file_number,
    url_function=None,
):
    try:
        print("scraping started")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(link, headers=headers, allow_redirects=True, timeout=10)

        response.raise_for_status()  # Check for any request errors

        soup = BeautifulSoup(response.content, "html.parser")
        print("extraction done")

        # Modify this part to extract the data you want from the BeautifulSoup object 'soup'
        data_to_store = soup.get_text()

        # Preprocess the data
        cleaned_data = preprocess_data(data_to_store)

        if url_function == "url_function":
            file_path = os.path.join("mysite", "demo_link_file", f"{file_number}.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(cleaned_data)

        else:
            file_path = os.path.join("mysite", "demo_files", f"{file_number}.txt")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(cleaned_data)

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {link}: {e}")

    except Exception as ex:
        print(f"An error occurred while scraping {link}: {ex}")


def save_data(query, url_function=None, url_links=None):
    if url_function == "url_function":
        for i, link in enumerate(url_links, start=1):
            scrape_and_store(
                link,
                file_number=i,
                url_function="url_function",
            )

    else:
        links = get_links(query)
        pattern = re.compile(r"(canada|revenuquebec)", re.IGNORECASE)
        print(links)
        # Select links with "canada" or "quebec" names
        selected_links = []
        for link in links:
            if link[12:].startswith("revenuquebec") or link[12:].startswith("canada"):
                selected_links.append(link)
        print(selected_links)
        # Loop through each link and scrape data
        for i, link in enumerate(selected_links, start=1):
            print("sent for scraping")
            scrape_and_store(link, file_number=i)
