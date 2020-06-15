from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 


class HelloMarket:
    def __init__(self):
        self.br = webdriver.Chrome('chromedriver')

    def login(self, id, pw):
        """
        captcha 우회...
        """
        pass 

    def get_item_num(self):
        soup = BeautifulSoup(self.br.page_source,'html.parser')
        products = soup.find_all('li',{'class':'main_col_3'})
        return products 
        
    def get_source(self, soup):
        title = soup.find('span',{'class':'item_title'}).text
        price = soup.find('div',{'class':'item_price item_price_bottom'}).text
        content = soup.find('div',{'class':'description_text'}).text
        return Content(title, price, content)

    def crawl_by_company(self, name, page):

        params = {'삼성':'1','애플':'2','엘지':'3'}
        br = self.br
        contents_list = []

        # 총 n 페이지 크롤링 
        pages = [i for i in range(0,int(page))]
        base_url = 'https://www.hellomarket.com'

        for page in pages:
            url = 'https://www.hellomarket.com/search?category=HAK001'+params[name]+'&page='+str(page)
            br.get(url)
            time.sleep(2)
            
            products = self.get_item_num() 
            for product in products:
                plus_url = product.find('a',{'class':'card card_list'}).attrs['href']
                url = base_url+plus_url
                br.get(url)

                soup = BeautifulSoup(br.page_source,'html.parser')
                
                time.sleep(3)

                ## 로그인 페이지인지 확인 (로그인 페이지 만나면 None 반환 )
                check_page = soup.find('span',{'class':'item_title'})

                if check_page == None:
                    br.get(url)
                    time.sleep(1)
                    soup = BeautifulSoup(br.page_source,'html.parser')
                    content = self.get_source(soup)
                    content.print()
                    content.filter_tel()
                    contents_list.append(content)
                else:
                    content = self.get_source(soup)
                    content.print()
                    contents_list.append(content)
            break
        return contents_list


import re 
class Content:
    def __init__(self,title,price,content):
        self.title = title 
        self.price = price 
        self.content = content
    
    def filter_model(self):
        title = self.title
        content = self.content 
    
    def filter_tel(self):
        content = self.content
        regex = re.compile('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        phone = re.search(regex, content)
        if phone[0] != None & len(phone[0]) == 11:
            print(phone[0])
        else:
            

    def print(self):
        print('TITLE:{}'.format(self.title))
        print('PRICE:{}'.format(self.price))
        print('CONTENT:{}'.format(self.content))

    

if __name__ == "__main__":
    from dbModel import DBModel
    
    conn = DBModel()
    hm = HelloMarket()


    content_list = hm.crawl_by_company('삼성',page=1)
    # for content in content_list:
    #     conn.InsertProduct(content)
        

