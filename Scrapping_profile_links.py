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


# specifies the path to the chromedriver.exe
driver = webdriver.Chrome(ChromeDriverManager().install())

# Two urls  one with opening the linkedIn second with flter (India)

urls = ['https://www.linkedin.com',"https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fsearch%2Fresults%2Fpeople%2F%3FgeoUrn%3D%255B%2522102713980%2522%255D%26keywords%3Dsolutions%2520engineer%26origin%3DFACETED_SEARCH&amp;fromSignIn=true&amp;trk=cold_join_sign_in"]
people = []
file_list = open('C:\\Users\\samee\\Desktop\\Stevens\\Third_Sem\\BIA 660 A\\Extra Credit\\filelist.txt','w',encoding='utf8')
#driver.get method() will navigate to a page given by the URL address
for i in range(len(urls)):
    try:
        driver.get(urls[i])
    except TimeoutException:
        print("Either Linkedin is not responding or Askijng for captcha Try after some time")
 
    if i == 0:
        username = driver.find_element_by_id('session_key')
        password = driver.find_element_by_id('session_password')
        username.send_keys('') #username

    if i == 1:
        password = driver.find_element_by_id('password')
   
    password.send_keys('')  #password
    if i == 0:
        button = driver.find_element_by_class_name('sign-in-form__submit-button')
    else:
         button = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')

    button.click()
    
    if i == 0:
        search = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))).click()
        WebDriverWait(driver, 10).until(
            expected_conditions.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']"))).send_keys('solutions engineer')


        driver.find_element_by_xpath("//*[@id='ember16']/input").send_keys(Keys.RETURN)

        people_page = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[aria-label=People]"))).click()

        time.sleep(3)
    
    no_of_people = 0

    i=0
    while i < 100:
        try:
            time.sleep(10)
            j = 0
            soup = BeautifulSoup(driver.page_source,'html.parser')
            links = soup.find_all('a', {'class':'app-aware-link ember-view search-result__result-link'})
            # for i in soup.find_all('h3', {'class':'actor-name-with-distance search-result__title single-line-truncate ember-view'}):
            for j in range(0,10):
                people.append(links[j]['href'])
                file_list.write('%s\n' %links[j]['href'])
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            people_page = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[aria-label=Next]"))).click()
            i = i+1
        except (TimeoutException,IndexError):
            retry_page = WebDriverWait(driver, 3).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[data-test=no-results-cta]"))).click()
            continue
file_list.close()
driver.close()