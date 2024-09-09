import requests
from bs4 import BeautifulSoup

urls_formations = [
    "https://ept.sn/presentation-de-lept/",
    "https://ept.sn/direction-des-etudes",
    "https://ept.sn/admission-et-cursus-a-lept/",
    "https://ept.sn/masters"
]

urls_departements = [
    "https://ept.sn/departements/tronc-commun",
    "https://ept.sn/departements/genie-electromecanique",
    "https://ept.sn/departements/genie-civil",
    "https://ept.sn/departements/genie-informatique-et-telecommunications"
]

def get_departements(urls=urls_departements):
    i = 1
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
        else:
            raise Exception(f"Server responded {response.status_code}")
        text_divs = soup.find_all("div", "jet-tabs__content")
        for text_div in text_divs:
            with open(f"documents/output_dpt{i}.txt", "a+") as f:
                f.write(text_div.text)
        i+=1        

def get_general(urls=urls_formations):
    i = 1
    for url in urls:
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
        else:
            raise Exception(f"Server responded {response.status_code}")
        text_divs = soup.find_all("div", "elementor-widget-container")
        for text_div in text_divs:
            with open(f"documents/output_formation{i}.txt", "a+") as f:
                f.write(text_div.text)
        i+=1

def get_direction(url = "https://ept.sn/direction-des-etudes/"):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
    else:
        raise Exception(f"Server responded {response.status_code}")
    col = soup.find("div", "elementor-col-66")
    text_divs = col.find_all("div", "elementor-widget-container")
    for text_div in text_divs:
        with open("documents/direction.txt", "w") as f:
            f.write(text_div.text)


def get_concours(url = "https://concours.ept.sn"):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
    else:
        raise Exception(f"Server responded {response.status_code}")
    faqs = soup.find_all("div", class_="gdlr-core-accordion-item-content-wrapper")
    for faq in faqs:
        with open("documents/concours.txt", "a+") as f:
            f.write(faq.text)

def get_mitmn(url="https://master-mitmn.ept.sn"):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
    else:
        raise Exception(f"Server responded {response.status_code}")
    text_divs = soup.find_all("div", class_="gdlr-core-column-first")
    for text_div in text_divs:
        with open("documents/mitmn.txt", "a+") as f:
            f.write(text_div.text)


get_general()
get_departements()
get_direction()
get_concours()
get_mitmn()