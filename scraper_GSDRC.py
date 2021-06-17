import os
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver

def download_publication(page_url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options,)
    driver.get(page_url)
    time.sleep(0.5)
    page = driver.page_source.strip()
    soup = BeautifulSoup(page, 'lxml')
    check = soup.find_all("a", class_="download")
    if check:
        publication_url = check[0].get('href')
        publication_url = publication_url.split('?')[0]
        driver.quit()
        if 'GSDRC' not in os.getcwd():
            os.makedirs('GSDRC')
            os.chdir('GSDRC')
        os.system('axel {}'.format(publication_url))
        return True
    return False


if __name__ == "__main__":
    count = 0
    for page_num in range(50):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=chrome_options,)
        main_url = 'https://gsdrc.org/?sfid=47074&_sft_gsdrc_pub_type=conflict-analyses%2Ce-learning%2Chelpdesk&sf_paged={}'
        driver.get(main_url.format(page_num + 1))
        time.sleep(0.5)
        main_page = driver.page_source.strip()
        main_soup = BeautifulSoup(main_page, 'lxml')

        for article in main_soup.find_all('article'):
            for heading in article.find_all('h2'):
                for link in heading.find_all('a'):
                    article_url = link.get('href')
            if download_publication(article_url):
                count+=1
        driver.quit()
    print("Downloaded {} articles!".format(count))
