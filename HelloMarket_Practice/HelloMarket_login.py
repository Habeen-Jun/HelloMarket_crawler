from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
br = webdriver.Chrome('chromedriver')
action = webdriver.ActionChains(br)
br.get('https://account.hellomarket.com/login?continue_url=https%3A%2F%2Fwww.hellomarket.com%2Fsearch%3Fcategory%3DHAK0011%26page%3D1')
time.sleep(1)
# br.find_element_by_xpath('//*[@id="__next"]/div/div[2]/form/div[1]/input').send_keys('junhabin@gmail.com')
# time.sleep(1)
# br.find_element_by_xpath('//*[@id="__next"]/div/div[2]/form/div[2]/input').send_keys('jih4412')
action.send_keys(Keys.TAB).send_keys(Keys.TAB).send_keys(Keys.ENTER).perform()

iframes = br.find_elements_by_tag_name('iframe')


time.sleep(1)
br.switch_to.frame(iframes[0])
element = br.find_element_by_class_name('recaptcha-checkbox-border')
br.execute_script("arguments[0].click();", element)


 




soup = BeautifulSoup(br.page_source,'html.parser')


# soup.find('div',{'class':'recaptcha-checkbox-border'})

# class HelloMarket:
    # def login(self, id, pw):
        # pass 
