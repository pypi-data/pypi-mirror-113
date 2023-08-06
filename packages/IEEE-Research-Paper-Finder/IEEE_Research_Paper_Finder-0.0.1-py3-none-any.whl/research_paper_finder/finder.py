from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import os
import glob
from os.path import basename
import requests
import json
import urllib.parse
import csv

def main() : 

    START_PAGE = 1
    LIST_LEN = 0
    data = []
    count = 0

    BASE_DIR = os.path.join(os.path.expanduser('~'),'Documents','IEEE Research Papers (CSV & JSON)')
    print(BASE_DIR)
    if not os.path.exists(BASE_DIR) :
        os.mkdir(BASE_DIR)
        print("Directory '%s' created" %BASE_DIR)
    else :
        print("Directory '%s' exists" %BASE_DIR)

    chromedriver_autoinstaller.install()  
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    # driver = webdriver.Chrome(executable_path=r".\research_paper_finder\chromedriver.exe",options = options)
    driver = webdriver.Chrome(options = options)
    query = str(input("Search here -> "))

    while True :

        url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&highlight=true&returnFacets=ALL&returnType=SEARCH&matchPubs=true&pageNumber={str(START_PAGE)}&queryText={str(query)}"
        driver.get(url)
        time.sleep(5)

        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        st_divs_all = soup.find_all('div',{"class" : "List-results-items"})
        print(len(st_divs_all))
        LIST_LEN += len(st_divs_all)

        for st_divs in st_divs_all :

            TITLE = ''
            PROFILE_URL = ''
            DOI = ''
            PDF_URL = ''
            DOI_URL = ''
            ABSTRACT = ''

            print("*"*20)
            

            # abstract = st_divs.find('i',{"class" : "icon-caret-abstract color-xplore-blue"})
            title = st_divs.find('a').text
            url_profile = st_divs.find('a')['href']
            url_profile = "https://ieeexplore.ieee.org" + url_profile
            print(title,'****',url_profile)
            TITLE = title
            PROFILE_URL = url_profile
            time.sleep(5)

            driver.get(url_profile)
            content = driver.page_source
            soup_doi = BeautifulSoup(content, "html.parser")
            soup_doi1 = soup_doi.find('div',{"class" : "abstract-desktop-div hide-mobile"})
            st_divs = soup_doi1.find('div',{"class" : "u-pb-1 stats-document-abstract-doi"})
            
            # if abstract is not None : 
            if st_divs is not None :
                
                try :
                    abstract = soup_doi1.find('div',{"class" : "u-mb-1"}).find('div').text
                    print(abstract)
                    ABSTRACT = abstract
                except Exception as e :
                    print(e)
                    pass

                doi = st_divs.find('a',{"target" : "_blank"}).text
                DOI = doi
                print(doi)
                try : 
                    url_doi = "https://sci-hub.do/" + doi
                    print(url_doi)
                    DOI_URL = url_doi
                    time.sleep(5)

                    r_doi = requests.get(url_doi)
                    content = r_doi.text
                    soup_pdf = BeautifulSoup(content, "html.parser")
                    url_pdf = soup_pdf.find('iframe',{"id" : "pdf"})['src']
                    if 'https' not in url_pdf:
                        url_pdf = "https:" + url_pdf
                    print(url_pdf)
                    PDF_URL = url_pdf
                    # download_file(url_pdf,title)
                
                except Exception as e:
                    print(e)
                    pass
                time.sleep(5)
                    
            scraper_data = {}
            scraper_data['title'] = TITLE
            scraper_data['profile_url'] = PROFILE_URL
            scraper_data['doi'] = DOI
            scraper_data['doi_url'] = DOI_URL
            scraper_data['pdf_url'] = PDF_URL
            scraper_data['abstract'] = ABSTRACT
            data.append(scraper_data)

            with open(os.path.join(BASE_DIR,f'IEEE_research_paper_finder_{str(query)}.json'),'w') as json_file :
                json.dump(data,json_file,ensure_ascii=False, indent=1)

            with open(os.path.join(BASE_DIR,f'IEEE_research_paper_finder_{str(query)}.csv'), mode='w') as csv_file:

                csv_writer = csv.writer(csv_file)
                # fieldnames = ['title', 'profile_url', 'doi','doi_url','pdf_url','abstract']
                count = 0
                for data_item in data:
                    if count == 0:
                        header = data_item.keys()
                        csv_writer.writerow(header)
                        count += 1
                    csv_writer.writerow(data_item.values())
                

        if data == [] :
            raise Exception('No search Result Found . The data object is empty . Please run the Python File once again ')
            break 

        print(f"Total scraped Data --> {LIST_LEN}")
        decision = str(input("Do you want to continue scraping ???"))
        if decision == 'y' :
            START_PAGE +=1
        else : 
            print(f"Files are saved in {BASE_DIR} directory")
            break

    driver.quit()

if __name__ == '__main__':
    main()