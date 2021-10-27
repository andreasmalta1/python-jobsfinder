from bs4 import BeautifulSoup
import requests
import lxml

html_text = requests.get("https://www.keepmeposted.com.mt/jobs-in-malta/").text
soup = BeautifulSoup(html_text, "lxml")
jobs = soup.find_all("div", class_="job-list-item")
for job in jobs:
    company_name = job.find("h6", "job-subtitle m-0").a.text.lstrip()
    position_description = job.find("h4", "job-title mt-0 mb-2").a.text.lstrip()

    print(f"""
    Company Name: {company_name}
    Position Description: {position_description}
    _________________________________________
    """)


# Loop thorugh pages
~# Save in file check if job exists  - stop