# This programs scrapes the KeepMePosted.com and CareerJet.com websites to get a a list of psted of jobs and saves them
# in a text file

from bs4 import BeautifulSoup
import requests
import os
import time
from datetime import datetime, timedelta


# Function to search if job already exsts in text file for keep me posted
def search_file(site, job_code):
    file_name = f"{site}.txt"
    with open(file_name, 'r') as f:
        for line in f:
            if job_code in line:
                return True
    return False


# Function to search if job already exsts in text file for career jet
def search_career():
    company = "Company Name:"
    position = "Position:"
    jobs_company = []
    jobs_position = []
    with open("cj.txt", 'r') as f:
        for line in f:
            if company in line:
                (company_desc, company_value) = line.split(": ")
                company_value = company_value.strip()
                jobs_company.append(company_value)
            if position in line:
                (position_desc, position_value) = line.split(": ")
                position_value = position_value.strip()
                jobs_position.append(position_value)
    return jobs_company, jobs_position


def search_dictionary(company_list, position_list, company, position):
    for i in range(len(company_list)):
        if (company in company_list[i]) and (position in position_list[i]):
            return True
    return False

#  Prepares the jobs to be added in a dummy text file
def prepend_job(site):
    dummy_file = f"{site}_dummy.txt"
    file_name = f"{site}.txt"
    with open(file_name, 'r') as file_read, open(dummy_file, 'a') as file_write:
        for line in file_read:
            file_write.write(line)
    os.remove(file_name)
    os.rename(dummy_file, file_name)


# Appends the jobs to the text file
def append_job(site, company_name, position_description, job_link, job_code):
    file_name = f"{site}_dummy.txt"
    with open(file_name, 'a') as f:
        f.write(f"Company Name: {company_name}\n")
        f.write(f"Position: {position_description}\n")
        f.write(f"Link: {job_link}\n")
        f.write(f"Job Code: {job_code}\n")
        today = datetime.now()
        today = today.strftime("%d-%m-%Y")
        f.write(f"Date Scraped: {today}\n")
        f.write("________________________________\n")


# Checks for internet connection
def check_internet():
    site_checker = "https://www.keepmeposted.com.mt"
    timeout = 5
    try:
        request = requests.get(site_checker, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False


# Scraping the keep me posted website
def keep_me_posted():
    page_num = 0
    counter = 0
    jobs_collected = 0
    site = "kmp"
    finish_loop = False
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    print(f"Collecting data from KeepMePosted.com at {now}")
    while not finish_loop:
        page_num += 1
        print(f"Collecting data from page number: {page_num}")
        url = f"https://www.keepmeposted.com.mt/jobs-in-malta/?pg={page_num}" \
              f"&per_page=21&order_by=date&order=DESC&keyword=&view_type=list"
        html = requests.get(url)
        if html.status_code == 404:
            now = datetime.now()
            now = now.strftime("%H:%M:%S")
            print(f"Collecting from KeepMePosted.com finished at {now}. Collected {jobs_collected} jobs")
            finish_loop = True
        else:
            html_text = html.text
            soup = BeautifulSoup(html_text, "lxml")
            jobs = soup.find_all("div", class_="job-list-item")
            for job in jobs:
                company_name = job.find("h6", class_="job-subtitle m-0").a.text.lstrip().rstrip()
                position = job.find("h4", class_="job-title mt-0 mb-2").a
                position_description = position.text.lstrip().rstrip()
                job_link = position["href"]
                job_code = job_link.split("-")[-1].replace("/", "")
                if not search_file(site, job_code):
                    append_job(site, company_name, position_description, job_link, job_code)
                    jobs_collected += 1
                else:
                    counter += 1
                    if counter == 15:
                        now = datetime.now()
                        now = now.strftime("%H:%M:%S")
                        print(f"Collecting from KeepMePosted.com finished at {now}. Collected {jobs_collected} jobs")
                        finish_loop = True
    prepend_job(site)


# Scraping the career jets website
def career_jet():
    page_num = 0
    counter = 0
    career_url = "https://www.careerjet.com.mt"
    jobs_collected = 0
    site = "cj"
    finish_loop = False
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    print(f"Collecting data from CareerJets.com at: {now}")
    while not finish_loop:
        page_num += 1
        print(f"Collecting data from page number: {page_num}")
        url = f"https://www.careerjet.com.mt/jobs-in-malta-island-120790.html?radius=0&p={page_num}&sort=date"
        html = requests.get(url)
        company_list, position_list = search_career()
        if html.status_code == 404 or html.status_code == 403:
            now = datetime.now()
            now = now.strftime("%H:%M:%S")
            print(f"Collecting from CareerJets.com finished at {now}. Collected {jobs_collected} jobs")
            print("Recollecting in 1 hour")
            finish_loop = True
        else:
            html_text = html.text
            soup = BeautifulSoup(html_text, "lxml")
            jobs = soup.find_all("article", class_="job clicky")
            for job in jobs:
                company_name = job.find("p", class_="company")
                if company_name is None:
                    pass
                else:
                    company_name = company_name.text.lstrip().rstrip()
                    position = job.find("header").h2.a
                    position_description = position.text.lstrip().rstrip()
                    more_info = position["href"]
                    job_link = f"{career_url}{more_info}"
                    job_code = "NA"
                    if not search_dictionary(company_list, position_list, company_name, position_description):
                        append_job(site, company_name, position_description, job_link, job_code)
                        jobs_collected += 1
                    else:
                        counter += 1
                        if counter == 10:
                            now = datetime.now()
                            one_hour = now + timedelta(hours=1)
                            now = now.strftime("%H:%M:%S")
                            one_hour = one_hour.strftime("%H:%M:%S")
                            print(f"Collecting from CareerJets.com finished at {now}. Collected {jobs_collected} jobs")
                            print(f"Recollecting in 1 hour @ {one_hour}")
                            finish_loop = True
    prepend_job(site)


# Programs runs every hourl intervals and displays how many new jobs it has found for each website
if __name__ == "__main__":
    print("Getting jobs from KeepMePosted and CareerJet at hourly intervals")
    while True:
        if check_internet():
            keep_me_posted()
            career_jet()
        else:
            print("No internet connection")
            print("Will try again in 1 hour")
        time.sleep(3600)
