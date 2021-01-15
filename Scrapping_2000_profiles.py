# Just for opening the file 
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions, expected_conditions
from selenium.webdriver.common.by import By  
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException,ElementNotInteractableException
from bs4 import BeautifulSoup
import time
import requests
import re
import csv
file_1 = open('C:\\Users\\samee\\Desktop\\Stevens\\Third_Sem\\BIA 660 A\\Extra Credit\\linkedin.csv','w',encoding='utf8')
csv_review = csv.writer(file_1,lineterminator='\n')
csv_review.writerow(['Name','[Comapny, Position ,(optional)sub_title]']
# to append the rows to the file
with open('C:\\Users\\samee\\Desktop\\Stevens\\Third_Sem\\BIA 660 A\\Extra Credit\\linkedin.csv','a',encoding='utf8', newline='') as file_2:
    csv_review = csv.writer(file_2)
    visually_hidden = 'visually-hidden'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.linkedin.com')
    username = driver.find_element_by_id('session_key')
    username.send_keys() #username
    password = driver.find_element_by_id('session_password')
    password.send_keys() #password
    button = driver.find_element_by_class_name('sign-in-form__submit-button').click() 
    time.sleep(10)       
    j=0

    with open('C:\\Users\\samee\\Desktop\\Stevens\\Third_Sem\\BIA 660 A\\Extra Credit\\filelistchunk.txt','r') as file_read:
        for line in file_read:
            if line == 'https://www.linkedin.com/search/results/people/headless?origin=SWITCH_SEARCH_VERTICAL&keywords=solutions%20engineer':
                continue
            print(j)
            if j%50 == 0:
                time.sleep(10)
            try: 
                name = None
                title_1 = None
                sub_title = None 
                cat_title = None
                comp = []
                companies=[]    
                driver.get(line)
                try:
                    # while driver.find_element_by_css_selector("button[class*='pv-profile-section__see-more-inline']"):
                    while expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "button[class*='pv-profile-section__see-more-inline']")):
                        driver.find_element_by_css_selector("button[class*='pv-profile-section__see-more-inline']").click()
                except (NoSuchElementException,ElementNotInteractableException):
                    pass
                responses = driver.page_source
                soup_people = BeautifulSoup(responses,'lxml')
                time.sleep(20)
                name = soup_people.find('li', {'class':'inline t-24 t-black t-normal break-words'}).text.strip()
                for compi in soup_people.findAll ('li', {'class':'pv-entity__position-group-pager pv-profile-section__list-item ember-view'}):
                        title = compi.find('h3',{'class':'t-16 t-black t-bold'})
                        if title.span != None:
                            title.span.decompose()
                        title_1 = title.text.strip()
                        # print(title_1)
                        sec_title = compi.find('p',{'class':'pv-entity__secondary-title t-14 t-black t-normal'})
                        if sec_title != None:
                            if sec_title.span != None:
                                sec_title.span.decompose()
                            sub_title = sec_title.text.strip()
                            #print(sub_title)
                        sub_cat = compi.find('ul',{'class':'pv-entity__position-group mt2'})
                        if sub_cat != None:
                            # print(sub_cat)
                            for sub in sub_cat.findAll({'h3':'t-14 t-black t-bold'}):
                                cat_title = sub.findAll('span')[-1].text.strip()
                                #print(cat_title)
                                #  
                        comp.append([sub_title,title_1,cat_title])
                companies.append(comp)
                csv_review.writerow([name,companies])
                j=j+1
            except (TimeoutException,IndexError,AttributeError):

                #sometimes it gets 
                    retry_page = WebDriverWait(driver, 3).until(
                    expected_conditions.presence_of_element_located((By.LINK_TEXT, "Sign in"))).click()
                    username = driver.find_element_by_id('username')
                    username.send_keys('') #username
                    password = driver.find_element_by_id('password')
                    password.send_keys() #password
                    button = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button').click()
                    continue

file_2.close()
driver.close()