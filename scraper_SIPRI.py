import os
import requests
from bs4 import BeautifulSoup

def download_publication(page_url):
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'lxml')
    #<a href="/sites/default/files/2019-11/pb_1911_eu_policy_on_climate-related_security_risks_0.pdf">DOWNLOAD FULL PUBLICATION</a>
    #https://www.sipri.org/sites/default/files/2019-11/pb_1911_eu_policy_on_climate-related_security_risks_0.pdf
    check = soup.find_all("a", string="DOWNLOAD FULL PUBLICATION")
    if check:
        publication_url = 'https://www.sipri.org' + check[0].get('href')
        if 'SIPRI' not in os.getcwd():
            os.makedirs('SIPRI')
            os.chdir('SIPRI')
        os.system('axel {}'.format(publication_url))
        return True
    return False


if __name__ == "__main__":
    count = 0
    for page_num in range(47):
        main_url = 'https://www.sipri.org/publications/search?keys=&author_editor=&field_associated_research_area_target_id=All&field_publication_type_target_id=All&page={}'
        main_page = requests.get(main_url.format(page_num))
        main_soup = BeautifulSoup(main_page.content, 'lxml')

        for em in main_soup.find_all('em'):
            for link in em.find_all('a'):
                article_url = 'https://www.sipri.org' + link.get('href')
                print(article_url)
                checker = download_publication(article_url)
                if checker:
                    count+=1
    print("Downloaded {} articles!".format(count))
