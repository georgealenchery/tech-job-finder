import requests
from database import insert_job

def scrape_remoteok(keyword="software"):
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed: {response.status_code}")
        return

    listings = response.json()
    count = 0

    for job in listings:
        if not isinstance(job, dict) or "position" not in job:
            continue

        title = job.get("position", "")
        if keyword.lower() not in title.lower():
            continue

        insert_job({
            "title": title,
            "company": job.get("company", "Unknown"),
            "location": job.get("location", "Remote"),
            "url": job.get("url", ""),
            "date_posted": job.get("date", ""),
            "source": "RemoteOK"
        })
        count += 1

    print(f"Inserted {count} jobs from RemoteOK")
    return count