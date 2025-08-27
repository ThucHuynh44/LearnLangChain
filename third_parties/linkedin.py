import os
import requests

from dotenv import load_dotenv

load_dotenv()


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    if mock:
        linkedin_profile_url = (
            "https://gist.github.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490"
        )
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.getenv("SCRAPING_API_KEY"),
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(api_endpoint, params=params, timeout=10)

    data = response.json().get("person", {})
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["schools"]
    }  # Remove empty fields

    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile("https://www.linkedin.com/in/tienhuynh1552/"))
