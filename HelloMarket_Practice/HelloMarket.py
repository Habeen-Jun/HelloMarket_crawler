from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import re


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
        
    def get_source(self, soup, company):
        title = soup.find('span',{'class':'item_title'}).text
        price = soup.find('div',{'class':'item_price item_price_bottom'}).text
        content = soup.find('div',{'class':'description_text'}).text
        return Content(title, price, content, company)

    def crawl_by_company(self, name, page):

        params = {'삼성':'1','애플':'2','엘지':'3'}
        br = self.br
        contents_list = []

        # 총 n 페이지 크롤링 
        pages = [i for i in range(1,int(page))]
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
                    content = self.get_source(soup,name)
                    content.print()
                    content.filter_tel()
                    content.filter_model()
                    contents_list.append(content)
                else:
                    content = self.get_source(soup,name)
                    content.print()
                    content.filter_model()
                    contents_list.append(content)
            break
        return contents_list


class Content:
    def __init__(self,title,price,content,company):
        self.company = company
        self.title = title 
        self.price = price 
        self.content = content
        self.model = self.filter_model()
        self.tel = self.filter_tel()
        
    
    def filter_model(self):
        title = self.title
        content = self.content

        grade = re.compile('\D급')
        model = re.search(grade,title)
        if model != None:
            model = model.end()
            model = title[:model]  
        else:
            grade = re.compile('\d기가|\dGB|\dG|\dgb|\dg')
            model = re.search(grade,title)
            if model != None:
                model = model.end()
                model = title[:model] 
            else:
                return title

        model_x = ['팝니다','(충전기 포함)','♡전문매장♡','판매합니다','단품','헬로페이','가성비굿~!','[당일배송]','정상해지','스마트폰','판매','미개봉','완박스']
        if model != None:
            for i in range(0,len(model_x)):
                model = model.replace(model_x[i],'')
        
        return model 
            
    def str_to_num(self,content):
        content = self.content
        content = content.strip()

        num_str = ['공','일','이','삼','사','오','육','칠','팔','구','십']
        
        for i in range(0,len(num_str)):
            content = content.replace(num_str[i],str(i))

        num_str2 = ['0⃣','1⃣','3⃣','4⃣','6⃣','8⃣','9⃣']
        num_str2_filter = [0,1,3,4,6,8,9]

        for i in range(0,len(num_str2)):
            content = content.replace(num_str2[i],str(num_str2_filter[i]))
        
        str_0 = ['o','O','ㅇ','영']
        
        for i in str_0:
            content = content.replace(i,'0')
        
        str_1 = ['l','I','ㅣ']

        for i in str_1:
            content = content.replace(i,'1')

        str_ = ['-','.','*','']

        for i in str_:
            content = content.replace(i,'')
        
        content = content.strip()
        return content 
    
    def filter_tel(self):
        content = self.content
        content = self.str_to_num(content)
        content = content.strip()

        f_regex = re.compile('\d{3}\S+\d{4}\S+\d{4}|\d{3}\s+\d{4}\s+\d{4}|\d{11,12}')
        phone = re.search(f_regex, content)
        
        if phone!= None:
            phone = phone[0].strip()
            return phone
        else:
            # print(content)
            return 'TEL does not exist'
            
            

    def print(self):
        print('COMPANY:{}'.format(self.company))
        print('TITLE:{}'.format(self.title))
        print('TEL:{}'.format(self.tel))
        print('MODEL:{}'.format(self.model))
        print('PRICE:{}'.format(self.price))
        print('CONTENT:{}'.format(self.content))
         

    

if __name__ == "__main__":
    from dbModel import DBModel
    
    conn = DBModel()
    hm = HelloMarket()

    company_list = ['삼성','엘지','애플']

    for company in company_list: 
        content_list = hm.crawl_by_company(company,page=5)
        for content in content_list:
            conn.InsertProduct(content)
        

