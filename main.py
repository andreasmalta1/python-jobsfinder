from bs4 import BeautifulSoup
import requests


def keep_me_posted():
    page_num = 0
    print("{:<50} {:<50} {:<20}".format('Company Name', 'Position', "Page"))
    while True:
        page_num += 1
        url = f"https://www.keepmeposted.com.mt/jobs-in-malta/?pg={page_num}&per_page=21&order_by=date&order=DESC&keyword=&view_type=list"
        html = requests.get(url)
        if html.status_code == 404:
            break
        else:
            html_text = html.text
            soup = BeautifulSoup(html_text, "lxml")
            jobs = soup.find_all("div", class_="job-list-item")
            for job in jobs:
                company_name = job.find("h6", "job-subtitle m-0").a.text.lstrip().rstrip()
                position_description = job.find("h4", "job-title mt-0 mb-2").a.text.lstrip().rstrip()
                print("{:<50} {:<50} {:<20}".format(company_name, position_description, page_num))


def career_jet():
    page_num = 0
    print("{:<50} {:<50} {:<20}".format('Company Name', 'Position', "Page"))
    while True:
        page_num += 1
        url = f"https://www.careerjet.com.mt/jobs-in-malta-island-120790.html?radius=0&p={page_num}&sort=date"
        html = requests.get(url)
        if html.status_code == 404:
            break
        else:
            html_text = html.text
            soup = BeautifulSoup(html_text, "lxml")
            jobs = soup.find_all("div", class_="job-list-item")
            for job in jobs:
                company_name = job.find("h6", "job-subtitle m-0").a.text.lstrip().rstrip()
                position_description = job.find("h4", "job-title mt-0 mb-2").a.text.lstrip().rstrip()
                print("{:<50} {:<50} {:<20}".format(company_name, position_description, page_num))


if __name__ == "__main__":
    print("Choose site to scrape job from")
    print("1. KeepMePosted")
    print("2. CareerJet")
    while True:
        response = input("Enter number: ")
        if response == "1":
            keep_me_posted()
            break
        elif response == "2":
            career_jet()
            break
        else:
            print("Invalid response")
